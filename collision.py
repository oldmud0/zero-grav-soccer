import math

from settings import COLLISION_ACCURACY

def aabb_swept_collision(r1, vel, r2):
    """Calculate a AABB swept collision, which compensates for
    sub-frame movement.
    Huge thanks to the people at gamedev.net:
    https://www.gamedev.net/resources/_/technical/game-programming/swept-aabb-collision-detection-and-response-r3084
    """
    vx = vel[0]
    vy = vel[1]

    inf = float("inf") # math.inf works only in Python 3.5

    # Find distance and time needed to reach collision on each axis
    # We need to calculate the distance between the closest and farthest edges
    # of the two objects.

    # Calculate inverse time
    if vx > 0:
        x_inv_entry = r2.x - (r1.x + r1.w)
        x_inv_exit = (r2.x + r2.w) - r1.x
    else:
        x_inv_entry = (r2.x + r2.w) - r1.x
        x_inv_exit = r2.x - (r1.x + r1.w)
    
    if vy > 0:
        y_inv_entry = r2.y - (r1.y + r1.h)
        y_inv_exit = (r2.y + r2.h) - r1.y
    else:
        y_inv_entry = (r2.y + r2.h) - r1.y
        y_inv_exit = r2.y - (r1.y + r1.h)

    # Find time of entry/exit for each axis
    if vx == 0:
        x_entry = -inf
        x_exit = inf
    else:
        x_entry = x_inv_entry / vx
        x_exit = x_inv_exit / vx

    if vy == 0:
        y_entry = -inf
        y_exit = inf
    else:
        y_entry = y_inv_entry / vy
        y_exit = y_inv_exit / vy

    # Which axis collided first?
    entry_time = max(x_entry, y_entry)
    exit_time = min(x_exit, y_exit)

    # No collision?
    if entry_time > exit_time or x_entry < 0 and y_entry < 0 or x_entry > 1 or y_entry > 1:
        # Collision won't happen within this frame.
        # return (collision_time, normal_x, normal_y)
        return 1, 0, 0
    else:
        if x_entry > y_entry:
            if x_inv_entry < 0:
                norm_x = 1
                norm_y = 0
            else:
                norm_x = -1
                norm_y = 0
        else:
            if y_inv_entry < 0:
                norm_x = 0
                norm_y = 1
            else:
                norm_x = 0
                norm_y = -1
        return entry_time, norm_x, norm_y

def simple_collision(mask, point, vel):
    """A simpler and less accurate method of calculating reflection angle.
    It only supports 90- and 45-degree slopes.
    """
    
    x_max, y_max = mask.get_size()
    
    u_pt = mask.get_at((point[0], max(0, point[1]-16)))
    d_pt = mask.get_at((point[0], min(y_max-1, point[1]+16)))
    
    l_pt = mask.get_at((max(0, point[0]-16), point[1]))
    r_pt = mask.get_at((min(x_max-1, point[0]+16), point[1]))
    
    if (l_pt ^ r_pt) and u_pt and d_pt: # Is this a vertical wall?
        return (-vel[0], vel[1])
    elif (u_pt ^ d_pt) and l_pt and r_pt: # Is it a horizontal wall?
        return (vel[0], -vel[1])
    elif (u_pt ^ d_pt) and (l_pt ^ r_pt): # Is it a diagonal wall?
        return (-vel[0], -vel[1])
    else:
        print("Collision warning: unusual wall -", l_pt, r_pt, u_pt, d_pt)
        return (-vel[0], -vel[1])
        
def elastic_collision(obj1, obj2, point):
    """Alter the velocities of two entities to simulate an elastic collision.
    Courtesy of https://metakatie.wordpress.com/2008/09/14/elastic-collision-conserved-momentum/
    v_1 = (m_1 - m_2)v_{1x} + 2m_2*v_{2x} / (m_1 + m_2)
    Sorry, my physics is rusting fairly quickly... :/
    """
    obj1.vx += ((obj1.mass - obj2.mass) * obj1.vx + 2 * obj2.mass * obj2.vx) / (obj1.mass + obj2.mass)
    obj1.vy += ((obj1.mass - obj2.mass) * obj1.vy + 2 * obj2.mass * obj2.vy) / (obj1.mass + obj2.mass)
    
    point_dist = point[0] - 8 + point[1] - 8 # Theoretical distance of collision from center of mass
    if point_dist != 0:
        obj1.vrot -= math.atan((obj2.vy + obj2.vx) / point_dist ) * point_dist
    
    obj2.vx -= ((obj2.mass - obj1.mass) * obj2.vx + 2 * obj1.mass * obj1.vx) / (obj1.mass + obj2.mass)
    obj2.vy -= ((obj2.mass - obj1.mass) * obj2.vy + 2 * obj1.mass * obj1.vy) / (obj1.mass + obj2.mass)
    
def calculate_reflection_angle(mask, point, vel):
    """Calculate an approximate plane from a mask for a reflection angle.
    This can be done by looking at the mask and tracing a line for a certain distance
    from a given point.
    """
    
    curr_point = point
    points = [curr_point]
    
    # Trace line right.
    for _ in range(COLLISION_ACCURACY):
        
        # Check if out of bounds.
        if curr_point[0] < 1 or curr_point[1] < 1:
            break # stop! stop!
        
        # Check if current spot is filled
        if mask.get_at(curr_point):
            points.append(curr_point)
        
        # Get points adjacent to current spot
        l = (curr_point[0]-1, curr_point[1])
        l_pt = mask.get_at(l)
        r = (curr_point[0]+1, curr_point[1])
        r_pt = mask.get_at(r)
        u = (curr_point[0], curr_point[1]-1)
        u_pt = mask.get_at(u)
        d = (curr_point[0], curr_point[1]+1)
        d_pt = mask.get_at(d)
        
        di_ur = (curr_point[0]+1, curr_point[1]-1)
        di_ur_pt = mask.get_at(di_ur)
        di_dr = (curr_point[0]+1, curr_point[1]+1)
        di_dr_pt = mask.get_at(di_dr)
        
        di_dl = (curr_point[0]-1, curr_point[1]+1)
        
        # Vertical:
        #  ? 1 ?      ? 0 ?      ? 1 ?      ? 0 ?
        #  ? x ?  or  ? x ?  or  ? x ?  or  ? x ?
        #  ? 0 ?      ? 1 ?      ? 1 ?      ? 0 ?
        v = u_pt << 1 | d_pt
        
        # Horizontal:
        #  ? ? ?      ? ? ?      ? ? ?      ? ? ?
        #  1 x 0  or  0 x 1  or  1 x 1  or  0 x 0 
        #  ? ? ?      ? ? ?      ? ? ?      ? ? ?
        h = l_pt << 1 | r_pt
        
        # Diagonal:
        #  ? ? 1      ? ? 0      ? ? 1      ? ? 0
        #  ? x ?  or  ? x ?  or  ? x ?  or  ? x ?
        #  ? ? 0      ? ? 1      ? ? 1      ? ? 0
        di_r = di_ur_pt << 1 | di_dr_pt
        
        # There are 2^9 combinations on this 3x3 grid,
        # but only 2^6 of them make sense. Let us continue.
        #if v == -1:
        #   if h == -1:
        #       if di_ur_pt:
        #           #   0 ?
        #           # 0 x 1
        #           #   1 ?
        #           curr_point = di_ur
        #       else:
        #           if di_dr_pt:
        #               curr_point = r
        #           else:
        #               curr_point = di_ur
        #           
        #   if h == 0:
        #       #   1  
        #       # 0 x 1
        #       #   0
        
        # Decision table favors rightward and downward movement
        # Dimensions: vertical, horizontal, diagonal
        path_table = [
        [[di_dl, di_dr, di_ur, di_dr],
         [r,     r,     r,     r    ],
         [l,     di_dr, di_ur, di_dr],
         [r,     r,     r,     di_dr]],
        [[d,     di_dr, d,     di_dr],
         [r,     r,     r,     d    ],
         [d,     di_dr, di_ur, di_dr],
         [r,     r,     di_ur, di_ur]],
        [[u,     di_dr, di_ur, di_dr],
         [r,     r,     r,     di_dr],
         [u,     di_dr, di_ur, di_dr],
         [r,     r,     r,     di_dr]],
        [[d,     di_dr, d,     di_dr],
         [r,     r,     d,     d],
         [d,     di_dr, d,     di_dr],
         [r,     r,     r,     di_dl]]]
         
        curr_point = path_table[v][h][di_r]
        
    try:
        slope = lsq_regression(points)
    except ZeroDivisionError: # Most likely a vertical wall.
        return (-vel[0], vel[1])
    
    slope_angle = math.degrees(math.atan(slope))
    normal = (math.cos(slope_angle), math.sin(slope_angle))
    dot_product_vec_normal = vel[0]*normal[0] + vel[1]*normal[1]
    
    reflected = (vel[0] - 2*dot_product_vec_normal * normal[0], vel[1] - 2*dot_product_vec_normal * normal[1])
    print("Angle of reflection:", slope_angle)
    print("Slope:", slope)
    
    return reflected
    

def lsq_regression(points):
    """Calculate least-squares regression of given list of points and return the slope."""
    # Calculate mean of X and Y values
    x_sum = 0
    y_sum = 0
    n = len(points)
    for point in points:
        x_sum += point[0]
        y_sum += point[1]
    x_mean = x_sum / n
    y_mean = y_sum / n
    
    # Calculate slope
    m_num_sum = 0
    m_denom_sum = 0
    for point in points:
        x_diff = (point[0] - x_mean)
        y_diff = (point[1] - y_mean)
        m_num_sum += x_diff * y_diff
        m_denom_sum += x_diff * x_diff
    slope = m_num_sum / m_denom_sum
    return slope

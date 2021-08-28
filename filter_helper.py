import ast

# Functions that apply filters
def apply_speed_v(vstream, speed_change):
    speed_change = max(0.05, speed_change)
    if(speed_change >= 0.5):
        vstream = vstream.filter('setpts', f'{1.0/speed_change}*PTS')
    else:
        current_speed = 1.0
        while(current_speed >= speed_change):
            if(current_speed * 0.5 <= speed_change):
                vstream = vstream.filter('setpts', f'{current_speed/speed_change}*PTS')
                break
            vstream = vstream.filter('setpts', '2*PTS')
            current_speed *= 0.5
    return vstream

def apply_speed_a(astream, speed_change):
    speed_change = max(0.05, speed_change)
    if(speed_change >= 0.5):
        astream = astream.filter('atempo', speed_change)
    else:
        current_speed = 1.0
        while(current_speed >= speed_change):
            if(current_speed * 0.5 <= speed_change):
                astream = astream.filter('atempo', speed_change/current_speed)
                break
            astream = astream.filter('atempo', 0.5)
            current_speed *= 0.5
    return astream

def apply_speed(vstream, astream, speed_change):
    vstream = apply_speed_v(vstream, speed_change)
    astream = apply_speed_a(astream, speed_change)
    return vstream, astream



# Functions that don't apply filters
def eval_arithmetic(expression):
    tree = None
    try:
        tree = ast.parse(expression, mode='eval')
    except SyntaxError:
        return None
    if not all(isinstance(node, (ast.Expression, ast.UnaryOp, ast.unaryop, ast.BinOp, ast.operator, ast.Num)) for node in ast.walk(tree)):
        return None
    
    return eval(compile(tree, filename='', mode='eval'))

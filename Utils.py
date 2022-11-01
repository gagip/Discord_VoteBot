def to_str_color(s, color):
    """
    디스코드 글씨 색을 바꿉니다
    디스코드 문법 참고: https://docs.google.com/document/d/1a93Obt9BDMGh-SL3quzU6OoyOJ3ZKN78Ez2CBA4FeEw/edit
    https://docs.google.com/document/d/1JxA085nOZgVIWXMPUrjJcGhX6MDVgZ1rD8OZ-hcYCmk/edit

    Parameter
    ---------
    s : str
        문자열
    color : str
        문자열(s)의 색깔

    Return
    ------
    result : str
        색깔이 바뀐 문자열
    """

    result = "```"
    if color == "red":
        result += "diff\n"
        result += "\n".join(["-" + line for line in s.split("\n")])
    elif color == "blue":
        result += "md\n"
        result += "\n".join(["#" + line for line in s.split("\n")])
    elif color == "yellow":
        result += "css\n"
    result += "```"
    return result


def to_long_string(long_str):
    """긴 문자열 처리"""
    return '\n'.join([line.strip() for line in long_str.splitlines()])
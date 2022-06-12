"""
@Author: yanzx
@Date: 2022/6/12 15:21
@Description: 
"""

def main():
    data = {
        "a": 1
    }
    res = map(str, data.values())
    print(list(res))


if __name__ == '__main__':
    main()
    print(int(True))
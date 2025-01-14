import pyautogui
import time
import os

# 定义获取输入的函数
def get_input(prompt, data_type=int):
    while True:
        try:
            return data_type(input(prompt))
        except ValueError:
            print(f"请输入有效的{data_type.__name__}。")

# 获取用户输入的坐标和参数
def get_coordinates():
    print("请输入截图区域的坐标：")
    x1 = get_input('位置_x1: ')         ## 619
    y1 = get_input('位置_y1: ')         ## 91
    x2 = get_input('位置_x2: ')         ## 1319
    y2 = get_input('位置_y2: ')         ## 1051
    xin = get_input('页码位置的x坐标: ')    ## 64
    yin = get_input('页码位置的y坐标: ')    ## 47（22到27行注释为文泉书局打开页面在edge浏览器全屏模式67%缩放，1080P分辨率下的参考坐标，可通过取消注释并把前面的函数注释掉来直接使用）
    return x1, y1, x2, y2, xin, yin

def get_parameters():
    num_screenshots = get_input('要截取的屏幕数量: ')
    interval = get_input('截图模块循环运行的间隔时间（秒，支持浮点数）: ', float)               # 可以设置的极短，就是每次截完图到下次翻页时的间隔时间
    sleep_time = get_input('每次运行中输入页码与执行截图间隔时间（秒，支持浮点数）: ', float)    # 这玩意得设高一点，文泉书局的阅读器效率太低最慢加载一张要20秒，为了减少返工的量，请至少设置10秒
    return num_screenshots, interval, sleep_time

# 设置截图保存的目录
save_directory = 'screenshots'
os.makedirs(save_directory, exist_ok=True)

# 主程序
def main():
    x1, y1, x2, y2, xin, yin = get_coordinates()
    num_screenshots, interval, sleep_time = get_parameters()

    # 确定截图区域的左上角和右下角坐标
    x, y = min(x1, x2), min(y1, y2)
    width, height = abs(x2 - x1), abs(y2 - y1)
    click_position = (xin, yin)            

    # 批量截图循环
    for i in range(num_screenshots):
        # 点击页码位置并输入的页码
        pyautogui.click(click_position)
        pyautogui.typewrite(i + 1)
        pyautogui.hotkey('enter')


        # 每次运行中输入页码与执行截图间隔时间（秒，支持浮点数）
        time.sleep(sleep_time)

        ##PAGE = int(input('page: '))                 # 手动截图保存页码设置

        # 截取指定区域的屏幕
        screenshot = pyautogui.screenshot(region=(x, y, width, height))
   
        # 保存截图
        try:
            ##screenshot.save(f'{save_directory}/screenshot_{PAGE}.png')       # 将此行与55行、65行取消注释，并注释63行与66行、47-49行，可进行手动截图，手动翻页到目标页面并输入当前截取的页码进行截图
            screenshot.save(f'{save_directory}/screenshot_{i + 1}.png')
            # 打印截图编号
            ##print(f'截图 {PAGE} 已保存。')
            print(f'截图 {i + 1} 已保存。')
        except Exception as e:
            print(f'保存截图时发生错误：{e}')
        
        # 截图模块循环运行的间隔时间（秒，支持浮点数）
        time.sleep(interval)

    print('所有截图已完成。')

if __name__ == "__main__":
    main()

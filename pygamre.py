# encoding:utf-8
_date_ = "2019/11/29 16:01"

import pygame
import random
import time
import os

def get_pic(path):
    # 拼接图片路径
    pic_path = os.path.join("/home/ti/PycharmProjects/feijidazhan/PlaneWars/img", path)
    # 返回pygame对象
    return pygame.image.load(pic_path)  # <Surface>

class Base:
    def __init__(self,x,y,screen):
        self.x=x
        self.y=y
        self.screen=screen

class Basebullet(Base):
    def __init__(self,x,y,screen):
        super().__init__(x,y,screen)
        self.pic=""
    def draw(self):
        self.screen.blit(self.pic,(self.x,self.y))
        self.move()
    def move(self):
        pass

class HeroBullet(Basebullet):
    """
    英雄精灵子弹的类
    """

    def __init__(self, x, y, screen):
        """
        :param x: x坐标
        :param y: y 坐标
        :param screen: 窗口对象
        """
        super().__init__(x,y,screen)
        self.pic = get_pic("bullet.png")

    def draw(self):
        """用来画子弹"""
        self.screen.blit(self.pic, (self.x, self.y))
        self.move()

    def move(self):
        self.y -= 5

class EnemyBullet(Basebullet):
    """敌机精灵子弹类"""

    def __init__(self, x, y, screen):
        super().__init__(x,y,screen)
        self.pic = get_pic("bullet1.png")

    # def draw(self):
    #     """用来画子弹"""
    #     self.screen.blit(self.pic, (self.x, self.y))
    #     self.move()

    def move(self):
        self.y += 5

class BasePlane(Base):
    def __init__(self,x,y,screen):
        super().__init__(x,y,screen)
        self.isBomb = False  # 碰撞检测
        self.bullet_list = []
        self.normal_image_index = 0
        self.bomb_image_index = 0

class HeroPlane(BasePlane):
    """英雄战机类"""
    def __init__(self, x, y, screen):
        super().__init__(x,y,screen)
        self.bomb_image_list = ["hero_blowup_n1.png", "hero_blowup_n2.png", "hero_blowup_n3.png","hero_blowup_n4.png", ]
        self.normal_image_list = ["hero1.png", "hero2.png"]

    def draw(self):

        if self.isBomb == False:  # 如果没有爆炸
            pic = get_pic(self.normal_image_list[self.normal_image_index])  # 获取图片
            self.screen.blit(pic, (self.x, self.y))  # 绘制英雄战机
            self.normal_image_index = (self.normal_image_index + 1) % len(self.normal_image_list)  # 利用取余运算进行循环
        else:
            if self.bomb_image_index == len(self.bomb_image_list):  # 当敌机爆炸图片的下表和图片总数相同时，说明爆炸图片已经绘制结束
                time.sleep(0.2)
                exit()
            enemy_bomb_img = get_pic(self.bomb_image_list[self.bomb_image_index])  # 加载英雄爆炸图片
            screen.blit(enemy_bomb_img, (self.x, self.y))  # 绘制敌机爆炸图片
            self.bomb_image_index += 1
            time.sleep(0.2)


    def deal_event(self, event_list):

        for event in event_list:
            if event.type == pygame.QUIT:  # 如果是退出事件
                exit(0)
            elif event.type == pygame.KEYDOWN:  # 检测鼠标按下事件
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.x = self.x - 10 if self.x >= 5 else 0
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:  # 向右移动
                    self.x = self.x + 10 if self.x <= 480 - 100 - 5 else 480 - 100
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:  # 向下移动
                    self.y = self.y + 10 if self.y <= 650 - 124 - 5 else 0
                elif event.key == pygame.K_q or event.key == pygame.K_UP:  # 向上移动
                    self.y = self.y - 10 if self.y >= 5 else 0
                elif event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    one_bullet = HeroBullet(self.x + 39, self.y - 22, screen)
                    self.bullet_list.append(one_bullet)
        # 绘制子弹
        for bullet in self.bullet_list:
            bullet.draw()
            self.bullet_list.remove(bullet) if bullet.y < 0 else ""

    def check_collide(self,bullet_list):
        """碰撞检测"""
        hero_rect = pygame.rect.Rect(self.x, self.y, 100, 124)
        # print(hero_rect)
        for bullet in bullet_list:
            enemy_bullet_rect = pygame.rect.Rect(bullet.x, bullet.y,9, 21)  # 定义英雄子弹的rect
            flag = enemy_bullet_rect.colliderect(hero_rect)  # 检测敌机和子弹的矩形是否相交
            if flag:
                print("英雄机爆炸了......")
                self.isBomb = True  # 英雄机爆炸条件为真
                bullet_list.remove(bullet) # 移除敌机子弹

class EnemyPlane(BasePlane):
    """敌机类"""
    def __init__(self, x, y, screen):
        super().__init__(x,y,screen)
        self.normal_image_list = ["enemy1.png"]
        self.normal_image_index = 0
        self.bomb_image_list = ["enemy1_down1.png", "enemy1_down2.png", "enemy1_down3.png", "enemy1_down4.png", ]
        self.bomb_image_index = 0
        self.isBomb = False
        self.bullet_list = []
        self.direct = "左"

    def draw(self):
        # 绘制
        if self.isBomb == False:  # 如果没有爆炸
            pic = get_pic(self.normal_image_list[self.normal_image_index])  # 获取图片
            self.screen.blit(pic, (self.x, self.y))  # 绘制敌机战机
            self.normal_image_index = (self.normal_image_index + 1) % len(self.normal_image_list)  # 利用循环让敌机进行循环
        else:
            if self.bomb_image_index == len(self.bomb_image_list):  # 当敌机爆炸图片的下表和图片总数相同时，说明爆炸图片已经绘制结束
                time.sleep(0.2)
                exit(0)  # 结束程序
            enemy_bomb_img = get_pic(self.bomb_image_list[self.bomb_image_index])  # 加载敌机爆炸图片
            screen.blit(enemy_bomb_img, (self.x, self.y))  # 绘制敌机爆炸图片
            self.bomb_image_index += 1
            time.sleep(0.2)
        # 调用移动函数
        self.move()
        # 敌机开火
        self.fire()

    def move(self):
        """让敌机移动"""
        if self.direct == "左":
            self.x -= 5
            if self.x <= 0:
                self.direct = "右"
        elif self.direct == "右":
            self.x += 5
            if self.x >= 480 - 69:
                self.direct = "左"

    def fire(self):
        """敌机子弹"""
        # 画出敌机子弹
        # 产生随机数
        x = random.randint(1, 100)
        if x == 5 or x == 78:
            # 实例化一个敌机子弹
            enemy_bullet = EnemyBullet(self.x + 69 // 2 - 9 // 2, self.y + 89, screen)
            # 产生的每一个子弹放到一个列表里
            self.bullet_list.append(enemy_bullet)
        for bullet in self.bullet_list:
            bullet.draw()  # 绘制子弹
            self.bullet_list.remove(bullet) if bullet.y > 700 - 89 - 21 // 2  else ""  # 让子弹到最下面的时候消失
    def check_collide(self,bullet_list):
        """"
        碰撞检测
        :param bullet_list: 英雄机子弹列表
        :return:
        """
        # 定义敌机精灵的rect
        enemy_rect = pygame.rect.Rect(self.x, self.y, 50, 56)  # x= 480//2-69//2
        print(enemy_rect)
        for bullet in bullet_list:
            hero_bullet_rect = pygame.rect.Rect(bullet.x, bullet.y, 22, 22)  # 定义英雄子弹的rect
            flag = hero_bullet_rect.colliderect(enemy_rect)  # 检测敌机和战机子弹的矩形是否相交
            if flag:
                print("敌机爆炸了......")
                self.isBomb = True  # 爆炸条件为真
                bullet_list.remove(bullet) # 移除战机子弹

if __name__ == '__main__':
    # 游戏初始化
    pygame.init()
    # 设置背景图片
    screen = pygame.display.set_mode((480, 700))
    # 设置标题
    pygame.display.set_caption("飞机大战")
    # 设置图标
    pygame.display.set_icon(get_pic("icon72x72.png"))
    # 设置按键灵敏度
    pygame.key.set_repeat(20, 30)
    # 实例化英雄飞机对象
    hero_plane = HeroPlane(190, 576, screen)
    # 实例化敌机对象
    enemy_plane = EnemyPlane(480 // 2 - 69 // 2, 0, screen)
    while True:
        # 绘制背景图
        screen.blit(get_pic("background.png"), (0, 0))
        #敌机碰撞检测
        enemy_plane.check_collide(hero_plane.bullet_list)
        #英雄机碰撞检测
        hero_plane.check_collide(enemy_plane.bullet_list)
        #绘制战机精灵
        hero_plane.draw()
        # 绘制敌机精灵
        enemy_plane.draw()
        # 事件检测
        hero_plane.deal_event(pygame.event.get())
        pygame.display.update()


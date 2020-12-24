import pygame
import os
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random
import math
import time

class Sphere:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = random.randint(-30,30)/5000
        self.vy = random.randint(-30,30)/5000
        self.vz = random.randint(-30,30)/5000

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def setVx(self, vxi):
        self.vx = vxi
    
    def setVy(self, vyi):
        self.vy = vyi
    
    def setVz(self, vzi):
        self.vz = vzi

    def invertVx(self):
        self.vx *= -1

    def invertVy(self):
        self.vy *= -1

    def invertVz(self):
        self.vz *= -1

class main:
    def __init__(self):
        self.vertices = (
            (1,-1,-1),
            (1,1,-1),
            (-1,1,-1),
            (-1,-1,-1),
            (1,-1,1),
            (1,1,1),
            (-1,-1,1),
            (-1,1,1)
            )
        self.edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7)
            )
        self.massa = 1
        self.spheres = []
        self.qtd = random.randint(1,50)
        self.light_pos = (0.05,1.0,-0.01,0.05)
        self.light_ambient = (0.0,2.0,2.3,1.0)
        self.light_diffuse = (0.0,2.0,2.0,1.0)
        self.light_specular = (2.0,5.0,2.0,1.0)
        self.rotateX = 1
        self.rotateY = 1
        self.rotateZ = 0
        self.veloRotate = 0

        self.display = (800,600)
        self.radius = 0.05

        self.lcm = str(round(1/(math.sqrt(2)*math.pi * pow(self.radius*2,2)*self.qtd/1), 6))

    def cube(self):
        glBegin(GL_LINES)
        for edge in self.edges:
            for vertex in edge:
                glColor3f(1,1,1)
                glVertex3fv(self.vertices[vertex])
        glEnd()
    
    def write(self, x, y, text):
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glColor3f(1,1,1)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glRasterPos2f(x,y)
        for i in text:
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ctypes.c_int(ord(i)))
        glDisable(GL_TEXTURE_2D)

    def drawSpheres(self):
        quad = gluNewQuadric()
        for k in self.spheres:
            glPushMatrix()
            glColor3f(1,1,1)
            glTranslatef(k.x,k.y,k.z)
            gluSphere(quad, self.radius, 70,70)
            glPopMatrix()
    
    def collision(self):

        def produtoInterno(a,b):
            total =  a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
            return total
        
        def produtoEscalarVet(a,b):
            return [a*b[0],a*b[1],a*b[2]]

        kEnergyX = 0
        kEnergyY = 0
        kEnergyZ = 0
        atual = 0
        collWall = 0

        for k in self.spheres:
            atual += 1
            if k.x >= 1 - self.radius or k.x <= -1 + self.radius:
                k.invertVx()
                collWall += 1
            if k.y >= 1 - self.radius or k.y <= -1 + self.radius:
                k.invertVy()
                collWall += 1
            if k.z >= 1 - self.radius or k.z <= -1 + self.radius:
                k.invertVz()
                collWall += 1
            cont = atual

            while cont < self.qtd:
                if (abs(k.x - self.spheres[cont].x)) <= self.radius *2:
                    if (abs(k.y - self.spheres[cont].y)) <= self.radius *2:                      
                        if (abs(k.z - self.spheres[cont].z)) <= self.radius *2:
                            cm = [ (k.x + self.spheres[cont].x)/2, (k.y + self.spheres[cont].y)/2, (k.z + self.spheres[cont].z)/2]
                            vb1 = produtoEscalarVet(produtoInterno([k.vx, k.vy,k.vz], cm)/ produtoInterno(cm,cm), cm)
                            vb2 = produtoEscalarVet(produtoInterno([self.spheres[cont].vx, self.spheres[cont].vy,self.spheres[cont].vz],cm)/produtoInterno(cm,cm),cm)
                            k.setVx(k.vx - vb1[0] + vb2[0])
                            k.setVy(k.vy - vb1[1] + vb2[1])
                            k.setVz(k.vz - vb1[2] + vb2[2])
                            self.spheres[cont].setVx(self.spheres[cont].vx - vb2[0] + vb1[0])
                            self.spheres[cont].setVy(self.spheres[cont].vy - vb2[1] + vb1[1])
                            self.spheres[cont].setVz(self.spheres[cont].vz - vb2[2] + vb1[2])
                cont += 1
            k.move()
            kEnergyX += self.massa * (k.vx*k.vx)/2
            kEnergyY += self.massa * (k.vy*k.vy)/2
            kEnergyY += self.massa * (k.vz*k.vz)/2
        kTotal = kEnergyX + kEnergyY + kEnergyZ
        #self.write(-2.5,0.28, "Kt: " + str(round(kTotal,6)))
        #self.write(-2.5,0.14, "Kx: " + str(round(kEnergyX,6)))
        #self.write(-2.5,0.0, "Ky: " + str(round(kEnergyY,6)))
        #self.write(-2.5,-0.14, "Kz: " + str(round(kEnergyZ,6)))
        #self.write(-2.5,-0.28, "p: " + str(round(kTotal,6)))
        return collWall
    def veloDistri(self):
        velo =  []
        for i in self.spheres:
            velo.append(round(math.sqrt(i.vx**2+i.vy**2+i.vz**2)*1000))

        velo = sorted(velo)

        veloGraph = []
        velocidadesUni = list(set(velo))
        i = 0
        while i < len(velocidadesUni):
            veloGraph.append(velo.count(velocidadesUni[i]))
            i+=1

            glBegin(GL_LINE_STRIP)
            glColor3f(1,1,1)
            glVertex2f(-3.01,-1.27)
            glVertex2f(-1.5,-1.27)
            glVertex2f(-1.5,-0.7)
            glVertex2f(-3.01,-0.7)
            glVertex2f(-3.01,-1.27)
            glEnd()

            i=2
            n=0
            pos = -3
            soma = 1.5/len(veloGraph)
            maxi= max(veloGraph)
            mini = min(veloGraph)
            fator = 0.5/self.qtd *5
            glBegin(GL_LINE_STRIP)
            while i < len(veloGraph):
                pos += soma
                glColor3f(1,1,1)
                y = veloGraph[i] * fator - 1.27
                glVertex2f(pos,y)
                i+=1
            glEnd()
            #self.write(-3,-1.41,"Distribuição de velocidades:")
    def colidiu(self, xk, yk, zk):
        for i in self.spheres:
            if(abs(xk - i.x)) <= self.radius * 2:
                if(abs(yk - i.y)) <= self.radius * 2:
                    if(abs(zk - i.z)) <= self.radius * 2:
                        return True
        return False
    
    def execute(self):
        i = 0
        while i < self.qtd:
            xk = random.uniform(-0.88,0.88)
            yk = random.uniform(-0.88,0.88)
            zk = random.uniform(-0.88,0.88)
            while self.colidiu(xk, yk, zk):
                xk = random.uniform(-0.88,0.88)
                yk = random.uniform(-0.88,0.88)
                zk = random.uniform(-0.88,0.88)
            self.spheres.append(Sphere(xk,yk,zk))
            i+=1
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF|OPENGL)
        pygame.display.set_caption("Simulador de gas")

        gluPerspective(45, (self.display[0]/self.display[1]),0.1,50.0)
        glTranslatef(0.8,0.0,-4.5)

        glLightfv(GL_LIGHT0, GL_POSITION, self.light_pos)
        glLightfv(GL_LIGHT0, GL_AMBIENT, self.light_ambient)
        glLightfv(GL_LIGHT0,GL_DIFFUSE, self.light_diffuse)
        glLightfv(GL_LIGHT0,GL_SPECULAR, self.light_specular)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glClear(GL_COLOR_BUFFER_BIT)

        glRotatef(GLfloat(1.0),GLfloat(1),GLfloat(1),GLfloat(0))

        begin = time.time()
        n = 0
        RODANDO = True
        while RODANDO:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RODANDO = False
                    break

                if event.type == pygame.KEYDOWN:

                    if event.key == K_w:
                        self.rotateX = 1
                        self.rotateY = 0
                        self.rotateZ = 0
                        self.veloRotate *= 1
                    
                    if event.key == K_s:
                        self.rotateX = 1
                        self.rotateY = 0
                        self.rotateZ = 0
                        self.veloRotate *= -1
                        
                    if event.key == K_a:
                        self.rotateX = 0
                        self.rotateY = 1
                        self.rotateZ = 0
                        self.veloRotate *= 1
                        
                    if event.key == K_d:
                        self.rotateX = 0
                        self.rotateY = 1
                        self.rotateZ = 0
                        self.veloRotate *= -1
                        
                    if event.key == K_q:
                        self.rotateX = 0
                        self.rotateY = 0
                        self.rotateZ = 1
                        self.veloRotate *= -1
                        
                    if event.key == K_e:
                        self.rotateX = 0
                        self.rotateY = 0
                        self.rotateZ = 1
                        self.veloRotate *= -1
                else:
                    self.veloRotate = 0.0
            if RODANDO:
                glRotatef(GLfloat(self.veloRotate), GLfloat(self.rotateX), GLfloat(self.rotateY), GLfloat(self.rotateZ))
                glClear(GL_COLOR_BUFFER_BIT)
                self.cube()
                n += self.collision()
                self.drawSpheres()
                end = time.time()
                tempo = end - begin
                #self.write(-2.5,0.42,"Time: "+ str(round(tempo, 2)))
                #self.write(-2.5,-0.42,"n: "+ str(round(n/tempo/6, 5)))
                #self.write(-2.5,-0.56,"lcm: "+ self.lcm)
                self.veloDistri()
                pygame.display.flip()
                pygame.time.wait(10)
            else: 
                pygame.quit()
            
iniciar = main()
iniciar.execute()


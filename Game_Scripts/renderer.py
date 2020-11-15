############################################################################
############################################################################

import pygame, math,pyglet
import Game_Scripts.sprites, Game_Scripts.tileMap, Game_Scripts.stage_Manager, Game_Scripts.functions, Game_Scripts.camera

#Functions
functions = Game_Scripts.functions

#Sprite Class
sprite = Game_Scripts.sprites.sprite

#tile Class
tile = Game_Scripts.tileMap.tile

#tile mapper
tile_mapper = Game_Scripts.tileMap

#stage functions
stage_manager = Game_Scripts.stage_Manager

#camera
camera_movement = Game_Scripts.camera

############################################################################
############################################################################

# #2D Renderer
# class camera2D():
#     def __init__(self, x, y, z):
#         self.x = x
#         self.y = y
#         self.z = z
#
# #Distort point from camera
# def distort2DCamera(x,y,cam,s):
#     nx = s.get_width()/2+cam.x-x
#     ny = s.get_height()/2+cam.y-y
#
#     return (nx,ny)
#
# #Draw the Sprite
# def drawSprite2D(spr, cam, s):
#     x = spr.x
#     y = spr.y
#     z = spr.z
#
#     # we need to reset the image because pygame.transform.scale is destructive and will no revert changes made
#     spr.img = functions.get_image(spr.imgUrl, True)
#
#     spr.img = pygame.transform.scale(spr.img, (spr.w, spr.h))
#
#     # flip based on heading
#     if spr.heading == "-":
#         spr.img = pygame.transform.flip(spr.img, True, False)
#
#     # replcae blit later with draw, when more sprites are done
#     #s.get_width/2 sets 0,0 to middle
#     #spr.w/2 sets spr to middle
#     s.blit(spr.img, (s.get_width()/2+cam.x-x-spr.w/2,s.get_height()/2+cam.y-y-spr.h))
#     #pygame.draw.circle(s, (255,255,255), (math.floor(s.get_width()/2+cam.x-x),math.floor(s.get_height()/2+cam.y-y)), 40, 0)
#
#
#
# #Draw Each Tile
# def drawTile2D(o, cam, s):
#     """
#     Front Face
#     0 - ------2
#     |         |
#     |         |
#     |         |
#     1 - ------3
#     """
#     #Define Vertice Coords
#     vt = []
#
#     vt.append([o.x - (o.w / 2), o.y - (o.h / 2), o.z])
#     vt.append([o.x - (o.w / 2), o.y + (o.h / 2) , o.z])
#     vt.append([o.x + (o.w / 2), o.y - (o.h / 2), o.z])
#     vt.append([o.x + (o.w / 2), o.y + (o.h / 2), o.z])
#
#     segments = [[0, 1], [1, 3], [2, 3], [0, 2]]
#     edges = []
#     dC =[]
#
#     for i in range(0, len(vt)):
#         x = vt[i][0]
#         y = vt[i][1]
#         z = vt[i][2]
#
#         dC.append(distort2DCamera(x,y,cam,s))
#         #dC.append(functions.distortPoint(x,y,z,cam,s))
#
#     # Define Coords for Segment
#     for i in range(0, len(segments)):
#         edges.append([dC[segments[i][0]], dC[segments[i][1]]])
#
#     # Fill the face of tiles that the sprites are standing on
#     if o.occupied == True:
#         #pygame.draw.polygon(s, o.fillColor, [dC[1], dC[3], dC[2], dC[0]], 0)
#
#         # print(edges)
#         # Draw Lines For Each Segment
#         for i in range(0, len(edges)):
#             pygame.draw.line(s, o.fillColor, [edges[i][0][0], edges[i][0][1]], [edges[i][1][0], edges[i][1][1]], 1)
#
#     # Fill the face of tiles that have an atk on them
#     hasAtk = False
#     if len(o.tileEffects) > 0:
#         for i in o.tileEffects:
#             if isinstance(i, tile_mapper.attack) == True:
#                 hasAtk = True
#     '''if hasAtk == True:
#         pygame.draw.polygon(s, (255, 85, 85), [dC[1], dC[3], dC[2], dC[0]], 0)
#         for i in range(0, len(edges)):
#             pygame.draw.line(s, (255, 85, 85), [edges[i][0][0], edges[i][0][1]], [edges[i][1][0], edges[i][1][1]], 5)'''


# #Draw Borders of Map
# def drawBorders2D(border, cam, s):
#     topCorner = border[0]
#     lowerCorner = border[1]
#
#     '''
#     0--------3
#     |        |
#     |        |
#     2--------1
#     '''
#
#     vt = []
#     vt.append([topCorner[0], topCorner[1], border[2]])
#     vt.append([lowerCorner[0], lowerCorner[1], border[2]])
#     vt.append([topCorner[0], lowerCorner[1], border[2]])
#     vt.append([lowerCorner[0], topCorner[1], border[2]])
#
#     segments = [[0, 3], [2, 1], [0, 2], [3, 1]]
#     edges = []
#     dC = []
#
#     for i in range(0, len(vt)):
#         x = vt[i][0]
#         y = vt[i][1]
#         z = vt[i][2]
#
#         dC.append(distort2DCamera(x,y,cam,s))
#         #dC.append(functions.distortPoint(x, y, z, cam, s))
#
#     '''for i in range(0, len(segments)):
#         edges.append([dC[segments[i][0]], dC[segments[i][1]]])
#
#     for i in range(0, len(edges)):
#         pygame.draw.line(s, (165,255,255), [edges[i][0][0], edges[i][0][1]], [edges[i][1][0], edges[i][1][1]], 1)'''
#     for i in range(0, len(segments)):
#         edges.append([dC[segments[i][0]], dC[segments[i][1]]])
#
#     for i in range(0, len(edges)):
#             pygame.draw.line(s, (65,255,255), [edges[i][0][0], edges[i][0][1]], [edges[i][1][0], edges[i][1][1]], 1)

#Render background
background_render_ticks = 0

tilesList = []

#Main Render Function for 2D
def flatRender(renderList, cam, borders, s, stage, background_screen, ch, w, h, vertexLists):

    tilesList.clear()

    global background_render_ticks, cam_thread

    camera_movement.determine_camera_position(ch, cam)

    d = []

    # Find Distance Between each object and camera
    for i in range(0, len(renderList)):

        x = renderList[i].x-cam.x
        y = renderList[i].y-cam.y
        z = renderList[i].z-cam.z

        #three dimensional space so not a just a z-index
        d.append(math.sqrt(x*x+y*y+z*z))

    #Sort the Distances from far to close
    sD = functions.copyArray(d)
    sD.sort()
    #sD.reverse()

    fRenderList = []

    # Match Each Sorted Value to actual Object
    for i in range(0, len(sD)):
        for i1 in range(0, len(d)):
            if (sD[i] == d[i1]):
                fRenderList.append(renderList[i1])

    #drawbackground first
    #'''
    background = stage_manager.renderStage2D(stage, background_screen, cam, 2, w, h)

    drawBorders2_5D(borders, cam, background_screen,w,h,vertexLists)

    x = w
    y = h

    #tiles before chr
    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], tile):
            drawTile2_5D(fRenderList[i], cam, background_screen,w,h,vertexLists)
            pass

    #background_screen.draw()

    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], sprite):
            #drawSprite2D(fRenderList[i], cam, s)
            group = pyglet.graphics.OrderedGroup(i)
            drawSprite3D(fRenderList[i], cam, s,w,h,vertexLists, group)
            pass

    #foreground_screen = pygame.Surface((x, y), pygame.SRCALPHA)
    #foreground
    foreground = stage_manager.renderStage2D(stage, s, cam, 1,w,h)
    #s.blit(foreground, (0,0))
    #'''
    '''
    background = stage_manager.renderStage2D(stage, background_screen, cam, 2)
    background.fill((55,55,55))

    drawBorders2_5D(borders, cam, background)

    x = s.get_width()
    y = s.get_height()

    tile_layer= pygame.Surface((x, y), pygame.SRCALPHA)

    #tiles before chr
    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], tile):
            drawTile2_5D(fRenderList[i], cam, tile_layer)
            pass
    background.blit(tile_layer, (0,0))
    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], sprite):
            #drawSprite2D(fRenderList[i], cam, s)
            drawSprite3D(fRenderList[i], cam, background)
            pass

    foreground_screen = pygame.Surface((x, y), pygame.SRCALPHA)
    #foreground
    foreground = stage_manager.renderStage2D(stage, foreground_screen, cam, 1)
    background.blit(foreground, (0,0))
    s.blit(background, (0, 0))
    '''



############################################################################
############################################################################

#3D Renderer

class camera3D():
    def __init__(self, x, y, z, xRot, yRot):
        self.x = x
        self.y = y
        self.z = z
        self.xRot = xRot
        self.yRot = yRot

def drawSprite3D(spr, cam, s,w,h, vertexLists, group):
    #update SpriteBox Location
    spr.spriteBox.updateSpriteBox(spr, cam, s,w,h)

    #we need to reset the image because pygame.transform.scale is destructive and will no revert changes made
    spr.img = functions.get_image(spr.imgUrl, True)

    # now we scale the image again
    # surface = pygame.Surface((spr.spriteBox.rect.width, spr.spriteBox.rect.height), pygame.SRCALPHA)
    # pygame.transform.scale(spr.img, (spr.spriteBox.rect.width, spr.spriteBox.rect.height), surface)
    #spr.img = pygame.transform.scale(spr.img, (spr.spriteBox.rect.width, spr.spriteBox.rect.height))
    #spr.img = functions.get_scaled_image(spr.img, spr.imgUrl, (spr.spriteBox.rect.width, spr.spriteBox.rect.height), 50)

    # flip based on heading
    spr.img.anchor_x = spr.img.width//2;
    #spr.img.anchor_y = 0;
    if spr.heading == "-":
        spr.img = spr.img.get_texture().get_transform(True, False, 0)

    edges2 = [
        [[spr.spriteBox.rect.x,spr.spriteBox.rect.y],
         [spr.spriteBox.rect.x+spr.spriteBox.rect.width,spr.spriteBox.rect.y]],
        [[spr.spriteBox.rect.x+spr.spriteBox.rect.width, spr.spriteBox.rect.y],
         [spr.spriteBox.rect.x+spr.spriteBox.rect.width, spr.spriteBox.rect.y+spr.spriteBox.rect.height]],
        [[spr.spriteBox.rect.x+spr.spriteBox.rect.width, spr.spriteBox.rect.y+spr.spriteBox.rect.height],
         [spr.spriteBox.rect.x, spr.spriteBox.rect.y + spr.spriteBox.rect.height]],
        [[spr.spriteBox.rect.x, spr.spriteBox.rect.y + spr.spriteBox.rect.height],
         [spr.spriteBox.rect.x,spr.spriteBox.rect.y]]
    ]
    edges = [
        [spr.spriteBox.vertexes[0],spr.spriteBox.vertexes[1]],
        [spr.spriteBox.vertexes[1], spr.spriteBox.vertexes[2]],
        [spr.spriteBox.vertexes[2], spr.spriteBox.vertexes[3]],
        [spr.spriteBox.vertexes[3], spr.spriteBox.vertexes[0]]
    ]

    for i in range(0, len(edges)):
        point_list = [edges[i][0][0], edges[i][0][1], edges[i][1][0], edges[i][1][1]]
        ec = int(len(point_list) / 2)
        vertexLists[len(vertexLists) + 1] = s.add(ec, pyglet.gl.GL_LINES, None,
                                                  ("v2f", point_list),
                                                  ("c3B", (255, 255, 255) * ec))
    # for i in range(0, len(edges2)):
    #     point_list = [edges2[i][0][0], edges2[i][0][1], edges2[i][1][0], edges2[i][1][1]]
    #     ec = int(len(point_list) / 2)
    #     vertexLists[len(vertexLists) + 1] = s.add(ec, pyglet.gl.GL_LINES, None,
    #                                               ("v2f", point_list),
    #                                               ("c3B", (255, 255, 0) * ec))

    xPos = int(spr.spriteBox.vertexes[2][0]+spr.spriteBox.xScale/2)
    yPos = spr.spriteBox.vertexes[2][1]

    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    #using pygletSprite
    spr.trueSpr = pyglet.sprite.Sprite(spr.img, xPos, yPos, batch=s, group=group)
    spr.trueSpr.scale = spr.spriteBox.yScale/spr.img.height

    #using own sprite model
    #spr.img.blit(xPos, yPos, zPos)

    #replcae blit later with draw, when more sprites are done
    #s.blit(surface, spr.spriteBox.rect)

# def drawTile(o, cam, s):
#     """
#     Top
#     Face
#     0 - ------3
#     |         |
#     |         |
#     |         |
#     1 - ------2
#     """
#     #Define Vertice Coords
#     vt = []
#
#     vt.append([o.x - (o.w / 2), o.y , o.z - (o.w / 2)])
#     vt.append([o.x - (o.w / 2), o.y , o.z + (o.w / 2)])
#     vt.append([o.x + (o.w / 2), o.y, o.z + (o.w / 2)])
#     vt.append([o.x + (o.w / 2), o.y, o.z - (o.w / 2)])
#
#     #For Each Coord Distort X,Y by (Inverse Z Difference)*Distance from Centre to Edge Horizontally
#     dC = []
#     #Draw Coordinates = dt
#
#     for i in range(0, len(vt)):
#         x = vt[i][0]
#         y = vt[i][1]
#         z = vt[i][2]
#
#         dC.append(functions.distortPoint(x,y,z,cam,s,w,h))
#
#     edges = []
#     segments = [[0, 1], [1, 2], [2, 3], [3, 0]]
#
#     """
#     ff segments: 01, 12, 23, 30
#     face connectors: 04, 15, 62, 37
#     bf segments: 45, 56, 67, 74
#     """
#
#     # Define Coords for Segment
#     for i in range(0, len(segments)):
#         edges.append([dC[segments[i][0]], dC[segments[i][1]]])
#
#     # print(edges)
#     # Draw Lines For Each Segment
#     for i in range(0, len(edges)):
#         pygame.draw.line(s, (165, 255, 255), [edges[i][0][0], edges[i][0][1]], [edges[i][1][0], edges[i][1][1]], 1)

# def render3D(drawList, cam, s):
#
#     d = []
#
#     # Find Distance Between each object and camera
#     for i in range(0, len(drawList)):
#         x = drawList[i].x - cam.x
#         y = drawList[i].y - cam.y
#         z = drawList[i].z - cam.z
#
#         d.append(math.sqrt(x * x + y * y + z * z))
#
#     # Sorted D
#     sd = functions.copyArray(d)
#     sd.sort()
#     sd.reverse()
#
#     # Final Shit
#     fList = []
#
#     # Match Each Sorted Value to actual Object
#     for i in range(0, len(sd)):
#         for i1 in range(0, len(d)):
#             if (sd[i] == d[i1]):
#                 fList.append(drawList[i1])
#
#     for i in range(0, len(fList)):
#         if isinstance(fList[i], sprite):
#             drawSprite3D(fList[i], cam, s)
#         elif isinstance(fList[i], tile):
#                 drawTile(fList[i], cam, s)

############################################################################
############################################################################

#2.5d RENDER

#Draw Each Tile
def drawTile2_5D(o, cam, s,w,h,vertexLists):
    """
    Front Face
    0 - ------2
    |         |
    |         |
    |         |
    1 - ------3
    """
    #Define Vertice Coords
    vt = []

    vt.append([o.x - (o.w / 2), o.y - (o.h / 2), o.z])
    vt.append([o.x - (o.w / 2), o.y + (o.h / 2) , o.z])
    vt.append([o.x + (o.w / 2), o.y - (o.h / 2), o.z])
    vt.append([o.x + (o.w / 2), o.y + (o.h / 2), o.z])

    segments = [[0, 1], [1, 3], [2, 3], [0, 2]]
    edges = []
    dC =[]

    for i in range(0, len(vt)):
        x = vt[i][0]
        y = vt[i][1]
        z = vt[i][2]

        #dC.append(distort2DCamera(x,y,cam,s))
        dC.append(functions.distortPoint(x,y,z,cam,s,w,h))

    # Define Coords for Segment
    for i in range(0, len(segments)):
        edges.append([dC[segments[i][0]], dC[segments[i][1]]])

    # Fill the face of tiles that the sprites are standing on

    if o.occupied == True:
        for i in range(0, len(edges)):
            point_list = [edges[i][0][0],edges[i][0][1], edges[i][1][0],edges[i][1][1]]
            ec = int(len(point_list) / 2)
            vertexLists[len(vertexLists)+1] = s.add(ec, pyglet.gl.GL_LINES, None,
                   ("v2f", point_list),
                                                    ("c3B", o.fillColor*ec))
         # point_list = [dC[2][0], dC[2][1], dC[3][0], dC[3][1], dC[1][0],dC[1][1], dC[0][0], dC[0][1]]
         # ec = int(len(point_list) / 2)
         # vertexLists[len(vertexLists)+1] = s.add(ec, pyglet.gl.GL_POLYGON, None,
         #       ("v2f", point_list))

    # Fill the face of tiles that have an atk on them
    hasAtk = False
    if len(o.tileEffects) > 0:
        for i in o.tileEffects:
            if isinstance(i, tile_mapper.attack) == True:
                hasAtk = True
    if hasAtk == True:
        for i in range(0, len(edges)):
            point_list = [edges[i][0][0],edges[i][0][1], edges[i][1][0],edges[i][1][1]]
            ec = int(len(point_list) / 2)
            vertexLists[len(vertexLists)+1] = s.add(ec, pyglet.gl.GL_LINES, None,
                   ("v2f", point_list),
                                                    ("c3B", (255,80,80)*ec))
    #     point_list = [dC[2][0], dC[2][1], dC[3][0], dC[3][1], dC[1][0],dC[1][1], dC[0][0], dC[0][1]]
    #     ec = int(len(point_list) / 2)
    #     vertexLists[len(vertexLists)+1] = s.add(ec, pyglet.gl.GL_POLYGON, None,
    #           ("v2f", point_list),
    #                                             ("c3B", (255,80,80)*ec))


#Draw Borders of Map
def drawBorders2_5D(border, cam, s,w,h, vertexLists):
    topCorner = border[0]
    lowerCorner = border[1]

    '''
    0--------3
    |        |
    |        |
    2--------1
    '''

    vt = []
    vt.append([topCorner[0], topCorner[1], border[2]])
    vt.append([lowerCorner[0], lowerCorner[1], border[2]])
    vt.append([topCorner[0], lowerCorner[1], border[2]])
    vt.append([lowerCorner[0], topCorner[1], border[2]])

    segments = [[0, 3], [2, 1], [0, 2], [3, 1]]
    edges = []
    dC = []

    for i in range(0, len(vt)):
        x = vt[i][0]
        y = vt[i][1]
        z = vt[i][2]

        #dC.append(distort2DCamera(x,y,cam,s))
        dC.append(functions.distortPoint(x, y, z, cam, s,w,h))

    for i in range(0, len(segments)):
         edges.append([dC[segments[i][0]], dC[segments[i][1]]])


    for i in range(0, len(edges)):
        point_list = [edges[i][0][0], edges[i][0][1], edges[i][1][0], edges[i][1][1]]
        ec = int(len(point_list) / 2)
        vertexLists[len(vertexLists) + 1] = s.add(ec, pyglet.gl.GL_LINES, None,
                                                  ("v2f", point_list),
                                                  ("c3B", (255,255,255) * ec))
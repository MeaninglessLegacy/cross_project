############################################################################
############################################################################



import math,\
    pyglet,\
    Game_Scripts.sprites,\
    Game_Scripts.tileMap,\
    Game_Scripts.stage_manager,\
    Game_Scripts.functions,\
    Game_Scripts.camera

#Functions
functions = Game_Scripts.functions

#Sprite Class
sprite = Game_Scripts.sprites.sprite

#tile Class
tile = Game_Scripts.tileMap.tile

#tile mapper
tile_mapper = Game_Scripts.tileMap

#stage functions
stage_manager = Game_Scripts.stage_manager

#camera
camera_movement = Game_Scripts.camera



############################################################################
############################################################################



class camera_3d():
    def __init__(self, x, y, z, xRot, yRot):
        self.x = x
        self.y = y
        self.z = z
        self.xRot = xRot
        self.yRot = yRot
        
        
        
############################################################################
############################################################################



tilesList = []



############################################################################
############################################################################



#Main Render Function for 2D
def flat_render(
        render_list,
        cam,
        borders,
        stage,
        chrList,
        mainBatch,
        backgroundBatch,
        window_w,
        window_h,
        batchedItems
):

    tilesList.clear()

    global cam_thread

    camera_movement.determine_camera_position(chrList, cam)

    d = []

    # Find Distance Between each object and camera
    for i in range(0, len(render_list)):

        x = render_list[i].x-cam.x
        y = render_list[i].y-cam.y
        z = render_list[i].z-cam.z

        #three dimensional space so not a just a z-index
        d.append(math.sqrt(x*x+y*y+z*z))

    #Sort the Distances from far to close
    sD = functions.copy_array(d)
    sD.sort()
    #sD.reverse()

    fRenderList = []

    # Match Each Sorted Value to actual Object
    for i in range(0, len(sD)):
        for i1 in range(0, len(d)):
            if (sD[i] == d[i1]):
                fRenderList.append(render_list[i1])

    #drawbackground first
    #'''
    background = stage_manager.render_stage(stage, backgroundBatch, cam, 2, window_w, window_h)

    draw_borders(borders, cam, backgroundBatch,window_w,window_h,batchedItems)

    x = window_w
    y = window_h

    #tiles before chr
    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], tile):
            draw_tiles(fRenderList[i], cam, backgroundBatch,window_w,window_h,batchedItems)
            pass

    #backgroundBatch.draw()

    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], sprite):
            #drawSprite2D(fRenderList[i], cam, mainBatch)
            group = pyglet.graphics.OrderedGroup(i)
            draw_sprite(fRenderList[i], cam, mainBatch,window_w,window_h,batchedItems, group)
            pass

    #foreground_screen = pygame.Surface((x, y), pygame.SRCALPHA)
    #foreground
    foreground = stage_manager.render_stage(stage, mainBatch, cam, 1,window_w,window_h)
    #mainBatch.blit(foreground, (0,0))
    #'''
    '''
    background = stage_manager.render_stage(stage, backgroundBatch, cam, 2)
    background.fill((55,55,55))

    draw_borders(borders, cam, background)

    x = mainBatch.get_width()
    y = mainBatch.get_height()

    tile_layer= pygame.Surface((x, y), pygame.SRCALPHA)

    #tiles before chr
    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], tile):
            draw_tiles(fRenderList[i], cam, tile_layer)
            pass
    background.blit(tile_layer, (0,0))
    for i in range(0, len(fRenderList)):
        if isinstance(fRenderList[i], sprite):
            #drawSprite2D(fRenderList[i], cam, mainBatch)
            draw_sprite(fRenderList[i], cam, background)
            pass

    foreground_screen = pygame.Surface((x, y), pygame.SRCALPHA)
    #foreground
    foreground = stage_manager.render_stage(stage, foreground_screen, cam, 1)
    background.blit(foreground, (0,0))
    mainBatch.blit(background, (0, 0))
    '''



def draw_sprite(spr, cam, s,window_w,window_h, batchedItems, group):
    #update SpriteBox Location
    spr.sprite_box.update_sprite_box(spr, cam, s,window_w,window_h)

    #we need to reset the image because pygame.transform.scale is destructive and will no revert changes made
    spr.img = functions.get_image(spr.imgUrl, True)

    # now we scale the image again
    # surface = pygame.Surface((spr.sprite_box.rect.width, spr.sprite_box.rect.height), pygame.SRCALPHA)
    # pygame.transform.scale(spr.img, (spr.sprite_box.rect.width, spr.sprite_box.rect.height), surface)
    #spr.img = pygame.transform.scale(spr.img, (spr.sprite_box.rect.width, spr.sprite_box.rect.height))
    #spr.img = functions.get_scaled_image(spr.img, spr.imgUrl, (spr.sprite_box.rect.width, spr.sprite_box.rect.height), 50)

    # flip based on heading
    spr.img.anchor_x = spr.img.width//2;
    #spr.img.anchor_y = 0;
    if spr.heading == "-":
        spr.img = spr.img.get_texture().get_transform(True, False, 0)

    #This is for debugging sprite boxes if they get of centered again

    # edges2 = [
    #     [[spr.sprite_box.rect.x,spr.sprite_box.rect.y],
    #      [spr.sprite_box.rect.x+spr.sprite_box.rect.width,spr.sprite_box.rect.y]],
    #     [[spr.sprite_box.rect.x+spr.sprite_box.rect.width, spr.sprite_box.rect.y],
    #      [spr.sprite_box.rect.x+spr.sprite_box.rect.width, spr.sprite_box.rect.y+spr.sprite_box.rect.height]],
    #     [[spr.sprite_box.rect.x+spr.sprite_box.rect.width, spr.sprite_box.rect.y+spr.sprite_box.rect.height],
    #      [spr.sprite_box.rect.x, spr.sprite_box.rect.y + spr.sprite_box.rect.height]],
    #     [[spr.sprite_box.rect.x, spr.sprite_box.rect.y + spr.sprite_box.rect.height],
    #      [spr.sprite_box.rect.x,spr.sprite_box.rect.y]]
    # ]
    # edges = [
    #     [spr.sprite_box.vertexes[0],spr.sprite_box.vertexes[1]],
    #     [spr.sprite_box.vertexes[1], spr.sprite_box.vertexes[2]],
    #     [spr.sprite_box.vertexes[2], spr.sprite_box.vertexes[3]],
    #     [spr.sprite_box.vertexes[3], spr.sprite_box.vertexes[0]]
    # ]

    # for i in range(0, len(edges)):
    #     point_list = [edges[i][0][0], edges[i][0][1], edges[i][1][0], edges[i][1][1]]
    #     ec = int(len(point_list) / 2)
    #     batchedItems[len(batchedItems) + 1] = s.add(ec, pyglet.gl.GL_LINES, None,
    #                                               ("v2f", point_list),
    #                                               ("c3B", (255, 255, 255) * ec))
    # for i in range(0, len(edges2)):
    #     point_list = [edges2[i][0][0], edges2[i][0][1], edges2[i][1][0], edges2[i][1][1]]
    #     ec = int(len(point_list) / 2)
    #     batchedItems[len(batchedItems) + 1] = s.add(ec, pyglet.gl.GL_LINES, None,
    #                                               ("v2f", point_list),
    #                                               ("c3B", (255, 255, 0) * ec))

    xPos = int(spr.sprite_box.vertexes[2][0]+spr.sprite_box.xScale/2)
    yPos = spr.sprite_box.vertexes[2][1]

    #Enable saving of alpha from the original sprite
    pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
    pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

    #create a new pyglet sprite if they don't have one or modify an exisitng sprite
    if spr.trueSpr != None:
        spr.trueSpr.image = spr.img
        spr.trueSpr.update(x=xPos, y=yPos, rotation=None, scale=spr.sprite_box.yScale/spr.img.height, scale_x=None, scale_y=None)
    else:
        spr.trueSpr = pyglet.sprite.Sprite(spr.img, xPos, yPos, batch=s, group=group)
        spr.trueSpr.scale = spr.sprite_box.yScale/spr.img.height



def draw_tiles(o, cam, s,window_w,window_h,batchedItems):
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
        dC.append(functions.distort_point(x,y,z,cam,s,window_w,window_h))

    # Define Coords for Segment
    for i in range(0, len(segments)):
        edges.append([dC[segments[i][0]], dC[segments[i][1]]])

    # Fill the face of tiles that the sprites are standing on

    if o.occupied == True:
        for i in range(0, len(edges)):
            point_list = [edges[i][0][0],edges[i][0][1], edges[i][1][0],edges[i][1][1]]
            ec = int(len(point_list) / 2)
            batchedItems[len(batchedItems)+1] = s.add(ec, pyglet.gl.GL_LINES, None,
                   ("v2f", point_list),
                                                    ("c3B", o.fillColor*ec))
         # point_list = [dC[2][0], dC[2][1], dC[3][0], dC[3][1], dC[1][0],dC[1][1], dC[0][0], dC[0][1]]
         # ec = int(len(point_list) / 2)
         # batchedItems[len(batchedItems)+1] = s.add(ec, pyglet.gl.GL_POLYGON, None,
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
            batchedItems[len(batchedItems)+1] = s.add(ec, pyglet.gl.GL_LINES, None,
                   ("v2f", point_list),
                                                    ("c3B", (255,80,80)*ec))
    #     point_list = [dC[2][0], dC[2][1], dC[3][0], dC[3][1], dC[1][0],dC[1][1], dC[0][0], dC[0][1]]
    #     ec = int(len(point_list) / 2)
    #     batchedItems[len(batchedItems)+1] = s.add(ec, pyglet.gl.GL_POLYGON, None,
    #           ("v2f", point_list),
    #                                             ("c3B", (255,80,80)*ec))



#Draw Borders of Map

def draw_borders(border, cam, s,window_w,window_h, batchedItems):
    '''
        0--------3
        |        |
        |        |
        2--------1
    '''
    topCorner = border[0]
    lowerCorner = border[1]

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
        dC.append(functions.distort_point(x, y, z, cam, s,window_w,window_h))

    for i in range(0, len(segments)):
         edges.append([dC[segments[i][0]], dC[segments[i][1]]])

    for i in range(0, len(edges)):
        point_list = [edges[i][0][0], edges[i][0][1], edges[i][1][0], edges[i][1][1]]
        ec = int(len(point_list) / 2)
        batchedItems[len(batchedItems) + 1] = s.add(ec, pyglet.gl.GL_LINES, None,
                                                  ("v2f", point_list),
                                                  ("c3B", (255,255,255) * ec))
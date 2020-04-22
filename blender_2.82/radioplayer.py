bl_info = {
    "name": "Radiola",
    "author": "nikitron.cc.ua",
    "version": (0, 0, 2),
    "blender": (2, 82, 0),
    "location": "View3D > Tool Shelf > SV > Radiola",
    "description": "Play the radio",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Create"}

import os
import signal
#import threading
import bpy
import time
import subprocess as sp
import aud

class OP_radiola(bpy.types.Operator):
    '''Radiola'''
    bl_idname = "sound.radiola"
    bl_label = "play radio"

    make : bpy.props.BoolProperty(name='make',default=False)
    clear : bpy.props.BoolProperty(name='clear',default=False)
    play : bpy.props.BoolProperty(name='play',default=True)
    item_play : bpy.props.IntProperty(name='composition',default=0)

    def execute(self, context):

        if self.clear:
            context.scene.rp_playlist.clear()
            context.window_manager.radiola_clear = True
            self.clear = False
            return {'FINISHED'} 
        if self.make:
            self.dolist(urls,names)
            context.window_manager.radiola_clear = False
            self.make = False
            return {'FINISHED'} 

        if not len(context.scene.rp_playlist):
            self.dolist(urls,names)
        url = context.scene.rp_playlist[self.item_play].url

        if self.play:
            context.window_manager.radiola_dev.stopAll()
            #music = sp.Popen(['/usr/bin/mplayer', url])
            context.window_manager.radiola_dev.play(aud.Sound(url))
            context.window_manager.radiola_ind = self.item_play
            #context.window_manager.radiola = music.pid
        else:
            #os.kill(context.window_manager.radiola, signal.SIGTERM)
            #music.terminate()
            context.window_manager.radiola_dev.stopAll()
        return {'FINISHED'} 

    def dolist(self,urls,names):
        for u,n in zip(urls,names):
            bpy.context.scene.rp_playlist.add()
            bpy.context.scene.rp_playlist[-1].url = u
            bpy.context.scene.rp_playlist[-1].name = n


class OP_radiola_panel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Misc"
    bl_context = "objectmode"
    bl_label = "Radiola"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        ''' \
        Radiola \
        '''
        layout = self.layout
        col = layout.column(align=True)
        col.scale_y = 1
        if context.window_manager.radiola_clear:
            col.operator('sound.radiola',text='Make').make = True
        else:
            col.operator('sound.radiola',text='Clear').clear = True
        col = layout.column(align=True)
        col.scale_y = 3
        b = col.operator('sound.radiola',text='Stop')
        b.play=False
        playlist_print = [a.name for a in context.scene.rp_playlist]
        i=0
        col = layout.column(align=True)
        col.scale_y = 1
        for p in playlist_print:
            i+=1
            if i == (context.window_manager.radiola_ind+1):
                a = col.operator('sound.radiola', text='> '+str(i)+' | '+str(p))
                a.item_play=i-1
                a.play=True
            else:
                a = col.operator("sound.radiola", text='    '+str(i)+' | '+str(p))
                a.item_play=i-1
                a.play=True

class RP_Playlist(bpy.types.PropertyGroup):
    url : bpy.props.StringProperty()
    name : bpy.props.StringProperty()

urls = [    'http://radio.6forty.com:8000/6forty',
            'http://postrocks.me:8000/',
            'http://79.111.14.76:8002/postrock',
			'http://79.120.39.202:8002/aabmds',
			'http://79.120.39.202:8002/darkambient',
			'http://79.120.39.202:8002/postmetal'
            'http://radios.rtbf.be/wr-c21-60-128.mp3',
            'http://radios.rtbf.be/wr-c21-70-128.mp3',
            'http://xstream1.somafm.com:8090',
            'http://streaming.koop.org:8534/',
            'http://ice.somafm.com/missioncontrol',
			'http://ice6.somafm.com/sonicuniverse-256-mp3',
			'http://ice2.somafm.com/spacestation-128-mp3',
			'http://ice.somafm.com/deepspaceone',
			'http://ice.somafm.com/dronezone',
			'http://s3.viastreaming.net:8835/',
			'http://37.251.146.169:8300/stream',
			
    ]
names = [   'PostRock',     '66forty',
            'PostRock',     'postrock.me',
            'RadioCaprice', 'PostRock',
			'RadioCaprice', 'Ambient Black Metal',
			'RadioCaprice', 'Darkambient',
			'RadioCaprice', 'Postmetal',
            'rtbf',         '60"s',
            'rtbf',         '70"s',
            'SomaFM',       'IndiePoP',
            'SomaFM',       'Koop', 
            'SomaFM',       'MissionControl',
            'SomaFM',       'SonicUniverse', 
            'SomaFM',       'Spacestation', 
            'SomaFM',       'Dronezone',
			'Darkambientradio', 'Darkambient',
			'Radio Classic', 'Mozart',
    ]

def dolist(urls,names):
    dic={}
    for u,n in zip(urls,names):
        #dic[n] = u
        bpy.context.scene.rp_playlist.add()
        bpy.context.scene.rp_playlist[-1].url = u
        bpy.context.scene.rp_playlist[-1].name = n
    #print(dic)

def register():
    try:
        if 'rp_playlist' in bpy.context.scene:
            bpy.context.scene.rp_playlist.clear()
    except:
        pass
    bpy.utils.register_class(RP_Playlist)
    bpy.types.Scene.rp_playlist = bpy.props.CollectionProperty(type=RP_Playlist)
    bpy.types.WindowManager.radiola_clear=bpy.props.BoolProperty(default=False)
    bpy.types.WindowManager.radiola=bpy.props.IntProperty()
    bpy.types.WindowManager.radiola_ind=bpy.props.IntProperty()
    bpy.types.WindowManager.radiola_dev = aud.Device()
    bpy.utils.register_class(OP_radiola)
    bpy.utils.register_class(OP_radiola_panel)

def unregister():
    bpy.utils.unregister_class(OP_radiola_panel)
    bpy.utils.unregister_class(OP_radiola)
    del bpy.types.WindowManager.radiola_ind
    del bpy.types.WindowManager.radiola
    del bpy.types.WindowManager.radiola_clear
    del bpy.types.Scene.rp_playlist


if __name__ == '__main__':
    register()

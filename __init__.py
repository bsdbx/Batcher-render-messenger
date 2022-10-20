# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Batcher - Render Messenger",
    "author" : "Bogdan", 
    "description" : "Addon + Telegram Bot That Notifies You About Render Events. So No More 'Render-Checks!'",
    "blender" : (3, 2, 0),
    "version" : (1, 0, 0),
    "location" : "Header -> Render",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "Render" 
}


import bpy
import bpy.utils.previews
from bpy.app.handlers import persistent
import requests
from datetime import datetime
import os


addon_keymaps = {}
_icons = None


def find_user_keyconfig(key):
    km, kmi = addon_keymaps[key]
    for item in bpy.context.window_manager.keyconfigs.user.keymaps[km.name].keymap_items:
        found_item = False
        if kmi.idname == item.idname:
            found_item = True
            for name in dir(kmi.properties):
                if not name in ["bl_rna", "rna_type"] and not name[0] == "_":
                    if not kmi.properties[name] == item.properties[name]:
                        found_item = False
        if found_item:
            return item
    print(f"Couldn't find keymap item for {key}, using addon keymap instead. This won't be saved across sessions!")
    return kmi


@persistent
def render_cancel_handler_3502C(dummy):
    id = bpy.context.scene.sna_telegram_chat_id
    date = str(datetime.now().date())
    time = str(datetime.now().time()).split(".")[0]
    render_engine = ('Workbench' if (bpy.context.scene.render.engine == 'BLENDER_WORKBENCH') else ('Eevee' if (bpy.context.scene.render.engine == 'BLENDER_EEVEE') else 'Cycles'))
    device = '                                                   Device: '
    dv = bpy.context.scene.cycles.device
    compositor = ('No' if (bpy.context.scene.use_nodes == False) else 'Yes')
    active_view_layer = bpy.context.view_layer.name
    display_device = bpy.context.scene.display_settings.display_device

    def canceled(text):
       token = "5675693027:AAGhGIFevPRkZD9Exovk_Inh7C0XEEtvFxQ"
       url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + id + "&text=" + text 
       results = requests.get(url_req)
       print(results.json())
    canceled("""          
              Error: Render Will Not Finish. It has probably been stopped by a user.                                      Date: """ +  date + '  Time: ' +  time  +        
              "                Render Engine: " + render_engine  +                 device + dv + '                                           Compositor Used: ' + compositor + '                                              Active View Layer: ' + active_view_layer
              + '                                  Display Device: ' + display_device)


@persistent
def render_complete_handler_5EDA9(dummy):
    id = bpy.context.scene.sna_telegram_chat_id
    date = str(datetime.now().date())
    time = str(datetime.now().time()).split(".")[0]
    render_engine = ('Workbench' if (bpy.context.scene.render.engine == 'BLENDER_WORKBENCH') else ('Eevee' if (bpy.context.scene.render.engine == 'BLENDER_EEVEE') else 'Cycles'))
    device = '                                                   Device: '
    dv = bpy.context.scene.cycles.device
    compositor = ('No' if (bpy.context.scene.use_nodes == False) else 'Yes')
    active_view_layer = bpy.context.view_layer.name
    display_device = bpy.context.scene.display_settings.display_device

    def canceled(text):
       token = "5675693027:AAGhGIFevPRkZD9Exovk_Inh7C0XEEtvFxQ"
       url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + id + "&text=" + text 
       results = requests.get(url_req)
       print(results.json())
    canceled("""          
              Render Finished!                                                       Date: """ +  date + '  Time: ' +  time  +        
              "                Render Engine: " + render_engine  +                 device + dv + '                                           Compositor Used: ' + compositor + '                                              Active View Layer: ' + active_view_layer
              + '                                  Display Device: ' + display_device)
    if bpy.context.scene.sna_output_image:
        pass
    else:
        os.remove(r"C:\Users\Bogdan\Desktop\0001.png")


@persistent
def render_init_handler_59A06(dummy):
    id = bpy.context.scene.sna_telegram_chat_id
    date = str(datetime.now().date())
    time = str(datetime.now().time()).split(".")[0]

    def started(text):
       token = "5675693027:AAGhGIFevPRkZD9Exovk_Inh7C0XEEtvFxQ"
       url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + id + "&text=" + text 
       results = requests.get(url_req)
       print(results.json())
    started("Render Started. Good Luck!" + '                                                          Date: ' + date + ' Time: ' + time)


def sna_add_to_topbar_mt_render_8EA94(self, context):
    if not (False):
        layout = self.layout
        layout.separator(factor=1.0)
        op = layout.operator('sna.batcher__renderer_9fee1', text='Batcher - Renderer', icon_value=258, emboss=True, depress=False)


class SNA_OT_Batcher__Renderer_9Fee1(bpy.types.Operator):
    bl_idname = "sna.batcher__renderer_9fee1"
    bl_label = "Batcher - Renderer"
    bl_description = "Render Image Considering It As The Animation"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        bpy.context.scene.render.filepath = bpy.context.scene.sna_text_file_path
        bpy.context.scene.frame_current = 1
        bpy.context.scene.frame_end = 1
        bpy.ops.render.render('INVOKE_DEFAULT', animation=True)
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        col_79655 = layout.column(heading='', align=False)
        col_79655.alert = False
        col_79655.enabled = True
        col_79655.active = True
        col_79655.use_property_split = False
        col_79655.use_property_decorate = False
        col_79655.scale_x = 1.0
        col_79655.scale_y = 1.0
        col_79655.alignment = 'Expand'.upper()
        col_79655.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_D72DC = col_79655.row(heading='', align=False)
        row_D72DC.alert = False
        row_D72DC.enabled = True
        row_D72DC.active = True
        row_D72DC.use_property_split = False
        row_D72DC.use_property_decorate = False
        row_D72DC.scale_x = 1.0
        row_D72DC.scale_y = 1.0
        row_D72DC.alignment = 'Expand'.upper()
        row_D72DC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if bpy.context.scene.sna_show_override:
            row_D72DC.prop(bpy.context.scene.render, 'use_overwrite', text='Overwrite', icon_value=0, emboss=True)
        if bpy.context.scene.sna_show_file_extensions:
            row_D72DC.prop(bpy.context.scene.render, 'use_file_extension', text='File Extensions', icon_value=0, emboss=True)
        row_45665 = col_79655.row(heading='', align=False)
        row_45665.alert = False
        row_45665.enabled = True
        row_45665.active = True
        row_45665.use_property_split = False
        row_45665.use_property_decorate = False
        row_45665.scale_x = 1.0
        row_45665.scale_y = 1.0
        row_45665.alignment = 'Expand'.upper()
        row_45665.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if bpy.context.scene.sna_show_cache_result:
            row_45665.prop(bpy.context.scene.render, 'use_render_cache', text='Cache Result', icon_value=0, emboss=True)
        if bpy.context.scene.sna_show_placeholders:
            row_45665.prop(bpy.context.scene.render, 'use_placeholder', text='Placeholders', icon_value=0, emboss=True)
        if bpy.context.scene.sna_show_file_format:
            col_79655.prop(bpy.context.scene.render.image_settings, 'file_format', text='File Format', icon_value=0, emboss=True)
        col_79655.separator(factor=0.550000011920929)
        if bpy.context.scene.sna_show_compression:
            col_79655.prop(bpy.context.scene.render.image_settings, 'compression', text='Comperssion', icon_value=0, emboss=True)
        col_79655.separator(factor=0.550000011920929)
        if bpy.context.scene.sna_show_render_camera:
            col_79655.prop(bpy.context.scene, 'camera', text='Render Cam', icon_value=0, emboss=True)
            col_79655.separator(factor=0.550000011920929)
            if bpy.context.scene.sna_show_render_engine:
                col_79655.prop(bpy.context.scene.render, 'engine', text='Engine', icon_value=0, emboss=True)
                col_79655.separator(factor=0.550000011920929)
                row_7E536 = col_79655.row(heading='', align=False)
                row_7E536.alert = False
                row_7E536.enabled = (bpy.context.scene.render.engine == 'CYCLES')
                row_7E536.active = True
                row_7E536.use_property_split = False
                row_7E536.use_property_decorate = False
                row_7E536.scale_x = 1.0
                row_7E536.scale_y = 1.0
                row_7E536.alignment = 'Expand'.upper()
                row_7E536.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                if bpy.context.scene.sna_show_device:
                    row_7E536.prop(bpy.context.scene.cycles, 'device', text='Device', icon_value=0, emboss=True)
        col_79655.separator(factor=0.550000011920929)
        row_3C44F = col_79655.row(heading='', align=True)
        row_3C44F.alert = False
        row_3C44F.enabled = True
        row_3C44F.active = True
        row_3C44F.use_property_split = False
        row_3C44F.use_property_decorate = False
        row_3C44F.scale_x = 1.0
        row_3C44F.scale_y = 1.0
        row_3C44F.alignment = 'Expand'.upper()
        row_3C44F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if bpy.context.scene.sna_show_samples_cycles:
            row_3C44F.prop(bpy.context.scene.cycles, 'samples', text='Sapmles(Cycles)', icon_value=0, emboss=True)
        if bpy.context.scene.sna_show_samples_eevee:
            row_3C44F.prop(bpy.context.scene.eevee, 'taa_render_samples', text='Sapmles(Eevee)', icon_value=0, emboss=True)
        split_5D5A7 = col_79655.split(factor=(1.0 if (bpy.context.scene.render.engine == 'BLENDER_WORKBENCH') else 0.8999999761581421), align=True)
        split_5D5A7.alert = False
        split_5D5A7.enabled = True
        split_5D5A7.active = True
        split_5D5A7.use_property_split = False
        split_5D5A7.use_property_decorate = False
        split_5D5A7.scale_x = 1.0
        split_5D5A7.scale_y = 1.0
        split_5D5A7.alignment = 'Center'.upper()
        split_5D5A7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_5D5A7.prop(bpy.context.scene, 'use_nodes', text='Use Compositor?', icon_value=0, emboss=True, toggle=True)
        op = split_5D5A7.operator('sna.batcher__view_layer_properties_f0859', text='', icon_value=117, emboss=True, depress=False)
        row_E3361 = col_79655.row(heading='', align=True)
        row_E3361.alert = False
        row_E3361.enabled = True
        row_E3361.active = True
        row_E3361.use_property_split = False
        row_E3361.use_property_decorate = False
        row_E3361.scale_x = 1.0
        row_E3361.scale_y = 1.0
        row_E3361.alignment = 'Expand'.upper()
        row_E3361.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_E3361.prop(bpy.context.scene.render, 'resolution_x', text='Resolution X:', icon_value=0, emboss=True)
        row_E3361.prop(bpy.context.scene.render, 'resolution_y', text='Resolution Y:', icon_value=0, emboss=True)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


class SNA_OT_Batcher__View_Layer_Properties_F0859(bpy.types.Operator):
    bl_idname = "sna.batcher__view_layer_properties_f0859"
    bl_label = "Batcher - View Layer Properties"
    bl_description = "View Layer Properties Settings"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        col_6E43F = layout.column(heading='', align=False)
        col_6E43F.alert = False
        col_6E43F.enabled = True
        col_6E43F.active = True
        col_6E43F.use_property_split = False
        col_6E43F.use_property_decorate = False
        col_6E43F.scale_x = 1.0
        col_6E43F.scale_y = 1.2999999523162842
        col_6E43F.alignment = 'Expand'.upper()
        col_6E43F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (bpy.context.scene.render.engine == 'BLENDER_EEVEE'):
            col_6E43F.popover('VIEWLAYER_PT_eevee_layer_passes_data', text='Data', icon_value=125)
        else:
            col_6E43F.popover('CYCLES_RENDER_PT_passes_data', text='Data', icon_value=125)
        if (bpy.context.scene.render.engine == 'BLENDER_EEVEE'):
            col_6E43F.popover('VIEWLAYER_PT_eevee_layer_passes_light', text='Light', icon_value=239)
        else:
            col_6E43F.popover('CYCLES_RENDER_PT_passes_light', text='Light', icon_value=239)
        if (bpy.context.scene.render.engine == 'BLENDER_EEVEE'):
            col_6E43F.popover('VIEWLAYER_PT_eevee_layer_passes_effects', text='Effects', icon_value=93)
        else:
            col_6E43F.popover('CYCLES_RENDER_PT_passes_light', text='Cryptomatte', icon_value=735)
        if (bpy.context.scene.render.engine == 'BLENDER_EEVEE'):
            col_6E43F.popover('VIEWLAYER_PT_layer_passes_cryptomatte', text='Cryptomatte', icon_value=735)
        else:
            col_6E43F.popover('CYCLES_RENDER_PT_filter', text='Filter', icon_value=688)
        if (bpy.context.scene.render.engine == 'BLENDER_EEVEE'):
            pass
        else:
            col_6E43F.popover('CYCLES_RENDER_PT_override', text='Override', icon_value=226)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=300)


class SNA_OT_Batcher__Check_For_Updates_2Fa96(bpy.types.Operator):
    bl_idname = "sna.batcher__check_for_updates_2fa96"
    bl_label = "Batcher - Check For Updates"
    bl_description = "Check wether current version is using"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        row_4841C = layout.row(heading='', align=False)
        row_4841C.alert = False
        row_4841C.enabled = True
        row_4841C.active = True
        row_4841C.use_property_split = False
        row_4841C.use_property_decorate = False
        row_4841C.scale_x = 1.0
        row_4841C.scale_y = 1.0
        row_4841C.alignment = 'Expand'.upper()
        row_4841C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_4841C.label(text='Version: ' + str(tuple((1, 0, 0))).replace('(1, 0, 0)', '1.0.0'), icon_value=0)
        if ((1, 0, 0) == (1.0, 0.0, 0.0)):
            row_4841C.label(text='           Using Current Version!', icon_value=0)
        else:
            row_7AF22 = row_4841C.row(heading='', align=False)
            row_7AF22.alert = True
            row_7AF22.enabled = True
            row_7AF22.active = True
            row_7AF22.use_property_split = False
            row_7AF22.use_property_decorate = False
            row_7AF22.scale_x = 1.0
            row_7AF22.scale_y = 1.0
            row_7AF22.alignment = 'Expand'.upper()
            row_7AF22.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_7AF22.label(text='New Version Is Avaliable', icon_value=2)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=310)


class SNA_AddonPreferences_634F4(bpy.types.AddonPreferences):
    bl_idname = 'batcher__render_messenger'

    def draw(self, context):
        if not (False):
            layout = self.layout 
            box_9AD5E = layout.box()
            box_9AD5E.alert = False
            box_9AD5E.enabled = True
            box_9AD5E.active = True
            box_9AD5E.use_property_split = False
            box_9AD5E.use_property_decorate = False
            box_9AD5E.alignment = 'Expand'.upper()
            box_9AD5E.scale_x = 1.0
            box_9AD5E.scale_y = 1.0
            box_9AD5E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_4B1E2 = box_9AD5E.column(heading='', align=True)
            col_4B1E2.alert = False
            col_4B1E2.enabled = True
            col_4B1E2.active = True
            col_4B1E2.use_property_split = False
            col_4B1E2.use_property_decorate = False
            col_4B1E2.scale_x = 1.0
            col_4B1E2.scale_y = 1.0
            col_4B1E2.alignment = 'Expand'.upper()
            col_4B1E2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_503A4 = col_4B1E2.row(heading='', align=True)
            row_503A4.alert = False
            row_503A4.enabled = True
            row_503A4.active = True
            row_503A4.use_property_split = False
            row_503A4.use_property_decorate = False
            row_503A4.scale_x = 1.0
            row_503A4.scale_y = 1.0
            row_503A4.alignment = 'Center'.upper()
            row_503A4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_503A4.label(text='Download Batcher - Render Messenger', icon_value=0)
            row_980D7 = col_4B1E2.row(heading='', align=True)
            row_980D7.alert = False
            row_980D7.enabled = True
            row_980D7.active = True
            row_980D7.use_property_split = False
            row_980D7.use_property_decorate = False
            row_980D7.scale_x = 1.0
            row_980D7.scale_y = 1.2999999523162842
            row_980D7.alignment = 'Expand'.upper()
            row_980D7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = row_980D7.operator('sn.dummy_button_operator', text='Blender Market', icon_value=0, emboss=True, depress=False)
            op = row_980D7.operator('sn.dummy_button_operator', text='Github', icon_value=0, emboss=True, depress=False)
            op = row_980D7.operator('sn.dummy_button_operator', text='Gumroad', icon_value=0, emboss=True, depress=False)
            op = col_4B1E2.operator('sna.batcher__check_for_updates_2fa96', text='Check For Updates', icon_value=73, emboss=True, depress=False)
            box_EF20C = layout.box()
            box_EF20C.alert = False
            box_EF20C.enabled = True
            box_EF20C.active = True
            box_EF20C.use_property_split = False
            box_EF20C.use_property_decorate = False
            box_EF20C.alignment = 'Center'.upper()
            box_EF20C.scale_x = 1.0
            box_EF20C.scale_y = 1.0
            box_EF20C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            split_2C97F = box_EF20C.split(factor=0.9544447064399719, align=True)
            split_2C97F.alert = False
            split_2C97F.enabled = True
            split_2C97F.active = True
            split_2C97F.use_property_split = False
            split_2C97F.use_property_decorate = False
            split_2C97F.scale_x = 1.0
            split_2C97F.scale_y = 1.0
            split_2C97F.alignment = 'Expand'.upper()
            split_2C97F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_E5E36 = split_2C97F.row(heading='', align=True)
            row_E5E36.alert = (len(bpy.context.scene.sna_telegram_chat_id) < 9)
            row_E5E36.enabled = True
            row_E5E36.active = True
            row_E5E36.use_property_split = False
            row_E5E36.use_property_decorate = False
            row_E5E36.scale_x = 1.0
            row_E5E36.scale_y = 1.0
            row_E5E36.alignment = 'Expand'.upper()
            row_E5E36.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_E5E36.prop(bpy.context.scene, 'sna_telegram_chat_id', text='Telegram Chat ID', icon_value=0, emboss=True)
            op = split_2C97F.operator('sn.dummy_button_operator', text='', icon_value=72, emboss=True, depress=False)
            row_DF8BA = box_EF20C.row(heading='', align=True)
            row_DF8BA.alert = False
            row_DF8BA.enabled = True
            row_DF8BA.active = True
            row_DF8BA.use_property_split = False
            row_DF8BA.use_property_decorate = False
            row_DF8BA.scale_x = 1.1710000038146973
            row_DF8BA.scale_y = 1.0
            row_DF8BA.alignment = 'Expand'.upper()
            row_DF8BA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_DB1CD = row_DF8BA.row(heading='', align=True)
            row_DB1CD.alert = False
            row_DB1CD.enabled = bpy.context.scene.sna_output_image
            row_DB1CD.active = True
            row_DB1CD.use_property_split = False
            row_DB1CD.use_property_decorate = False
            row_DB1CD.scale_x = 1.1710000038146973
            row_DB1CD.scale_y = 1.0
            row_DB1CD.alignment = 'Expand'.upper()
            row_DB1CD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_DB1CD.prop(bpy.context.scene, 'sna_text_file_path', text='Output Path', icon_value=0, emboss=True)
            row_DF8BA.prop(bpy.context.scene, 'sna_output_image', text='', icon_value=51, emboss=True)
            box_EF20C.prop(find_user_keyconfig('999EA'), 'type', text='Batcher - Renderer Shortcut', full_event=True)
            row_47F15 = layout.row(heading='', align=True)
            row_47F15.alert = False
            row_47F15.enabled = True
            row_47F15.active = True
            row_47F15.use_property_split = False
            row_47F15.use_property_decorate = False
            row_47F15.scale_x = 1.0
            row_47F15.scale_y = 1.2999999523162842
            row_47F15.alignment = 'Expand'.upper()
            row_47F15.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = row_47F15.operator('sna.batcher__switch_operator_3f4fa', text='Render Settings', icon_value=(13 if (bpy.context.scene.sna_preferences_switch == 'Render Settings') else 12), emboss=True, depress=(bpy.context.scene.sna_preferences_switch == 'Render Settings'))
            op.sna_enum_switch = 'Render Settings'
            op = row_47F15.operator('sna.batcher__switch_operator_3f4fa', text='View Layer Settings', icon_value=(12 if (bpy.context.scene.sna_preferences_switch == 'Render Settings') else 13), emboss=True, depress=(bpy.context.scene.sna_preferences_switch == 'View Layer Settings'))
            op.sna_enum_switch = 'View Layer Settings'
            box_B3841 = layout.box()
            box_B3841.alert = False
            box_B3841.enabled = True
            box_B3841.active = True
            box_B3841.use_property_split = False
            box_B3841.use_property_decorate = False
            box_B3841.alignment = 'Expand'.upper()
            box_B3841.scale_x = 1.0
            box_B3841.scale_y = 1.0
            box_B3841.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_4E03C = box_B3841.row(heading='', align=True)
            row_4E03C.alert = False
            row_4E03C.enabled = True
            row_4E03C.active = True
            row_4E03C.use_property_split = False
            row_4E03C.use_property_decorate = False
            row_4E03C.scale_x = 1.0
            row_4E03C.scale_y = 1.0
            row_4E03C.alignment = 'Expand'.upper()
            row_4E03C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.scene.sna_preferences_switch == 'Render Settings'):
                col_6F011 = row_4E03C.column(heading='', align=True)
                col_6F011.alert = False
                col_6F011.enabled = True
                col_6F011.active = True
                col_6F011.use_property_split = False
                col_6F011.use_property_decorate = False
                col_6F011.scale_x = 1.0
                col_6F011.scale_y = 1.0
                col_6F011.alignment = 'Expand'.upper()
                col_6F011.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_957B8 = col_6F011.row(heading='', align=True)
                row_957B8.alert = False
                row_957B8.enabled = True
                row_957B8.active = True
                row_957B8.use_property_split = False
                row_957B8.use_property_decorate = False
                row_957B8.scale_x = 1.0
                row_957B8.scale_y = 1.0
                row_957B8.alignment = 'Center'.upper()
                row_957B8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_957B8.label(text='Output Settings:', icon_value=84)
                row_A3A70 = col_6F011.row(heading='', align=True)
                row_A3A70.alert = False
                row_A3A70.enabled = True
                row_A3A70.active = True
                row_A3A70.use_property_split = False
                row_A3A70.use_property_decorate = False
                row_A3A70.scale_x = 1.0
                row_A3A70.scale_y = 1.0
                row_A3A70.alignment = 'Expand'.upper()
                row_A3A70.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_A3A70.prop(bpy.context.scene, 'sna_show_override', text='Show Override', icon_value=0, emboss=True, toggle=True)
                row_A3A70.prop(bpy.context.scene, 'sna_show_file_extensions', text='Show File Extentions', icon_value=0, emboss=True, toggle=True)
                row_DDE73 = col_6F011.row(heading='', align=True)
                row_DDE73.alert = False
                row_DDE73.enabled = True
                row_DDE73.active = True
                row_DDE73.use_property_split = False
                row_DDE73.use_property_decorate = False
                row_DDE73.scale_x = 1.0
                row_DDE73.scale_y = 1.0
                row_DDE73.alignment = 'Expand'.upper()
                row_DDE73.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_DDE73.prop(bpy.context.scene, 'sna_show_cache_result', text='Show Cache Result', icon_value=0, emboss=True, toggle=True)
                row_DDE73.prop(bpy.context.scene, 'sna_show_placeholders', text='Show Placeholders', icon_value=0, emboss=True, toggle=True)
                row_53FDA = col_6F011.row(heading='', align=True)
                row_53FDA.alert = False
                row_53FDA.enabled = True
                row_53FDA.active = True
                row_53FDA.use_property_split = False
                row_53FDA.use_property_decorate = False
                row_53FDA.scale_x = 1.0
                row_53FDA.scale_y = 1.0
                row_53FDA.alignment = 'Expand'.upper()
                row_53FDA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_53FDA.prop(bpy.context.scene, 'sna_show_file_format', text='Show File Format', icon_value=0, emboss=True, toggle=True)
                row_53FDA.prop(bpy.context.scene, 'sna_show_compression', text='Show Compression', icon_value=0, emboss=True, toggle=True)
                col_6F011.separator(factor=0.800000011920929)
                row_7E6ED = col_6F011.row(heading='', align=True)
                row_7E6ED.alert = False
                row_7E6ED.enabled = True
                row_7E6ED.active = True
                row_7E6ED.use_property_split = False
                row_7E6ED.use_property_decorate = False
                row_7E6ED.scale_x = 1.0
                row_7E6ED.scale_y = 1.0
                row_7E6ED.alignment = 'Center'.upper()
                row_7E6ED.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_7E6ED.label(text='Render Settings:', icon_value=258)
                row_C5C36 = col_6F011.row(heading='', align=True)
                row_C5C36.alert = False
                row_C5C36.enabled = True
                row_C5C36.active = True
                row_C5C36.use_property_split = False
                row_C5C36.use_property_decorate = False
                row_C5C36.scale_x = 1.0
                row_C5C36.scale_y = 1.0
                row_C5C36.alignment = 'Expand'.upper()
                row_C5C36.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_C5C36.prop(bpy.context.scene, 'sna_show_render_camera', text='Show Render Camera', icon_value=0, emboss=True, toggle=True)
                row_C5C36.prop(bpy.context.scene, 'sna_show_render_engine', text='Show Render Engine', icon_value=0, emboss=True, toggle=True)
                row_C5C36.prop(bpy.context.scene, 'sna_show_device', text='Show Device', icon_value=0, emboss=True, toggle=True)
                row_EC0D5 = col_6F011.row(heading='', align=True)
                row_EC0D5.alert = False
                row_EC0D5.enabled = True
                row_EC0D5.active = True
                row_EC0D5.use_property_split = False
                row_EC0D5.use_property_decorate = False
                row_EC0D5.scale_x = 1.0
                row_EC0D5.scale_y = 1.0
                row_EC0D5.alignment = 'Expand'.upper()
                row_EC0D5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                row_EC0D5.prop(bpy.context.scene, 'sna_show_samples_cycles', text='Show Samples(Cycles)', icon_value=0, emboss=True, toggle=True)
                row_EC0D5.prop(bpy.context.scene, 'sna_show_samples_eevee', text='Show Samples(Eevee)', icon_value=0, emboss=True, toggle=True)
            if (bpy.context.scene.sna_preferences_switch == 'View Layer Settings'):
                row_4E03C.label(text='2', icon_value=0)


class SNA_OT_Batcher__Switch_Operator_3F4Fa(bpy.types.Operator):
    bl_idname = "sna.batcher__switch_operator_3f4fa"
    bl_label = "Batcher - Switch Operator"
    bl_description = "Batcher - Preferences Switch"
    bl_options = {"REGISTER", "UNDO"}

    def sna_enum_switch_enum_items(self, context):
        return [("No Items", "No Items", "No generate enum items node found to create items!", "ERROR", 0)]
    sna_enum_switch: bpy.props.EnumProperty(name='Enum Switch', description='', items=[('Render Settings', 'Render Settings', '', 0, 0), ('View Layer Settings', 'View Layer Settings', '', 0, 1)])

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        bpy.context.scene.sna_preferences_switch = self.sna_enum_switch
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.types.Scene.sna_telegram_chat_id = bpy.props.StringProperty(name='Telegram Chat ID', description='', default='', subtype='PASSWORD', maxlen=0)
    bpy.types.Scene.sna_text_file_path = bpy.props.StringProperty(name='Text File Path', description='', default='', subtype='DIR_PATH', maxlen=0)
    bpy.types.Scene.sna_output_image = bpy.props.BoolProperty(name='Output Image', description='Output Image To Specific Directory', default=True)
    bpy.types.Scene.sna_preferences_switch = bpy.props.EnumProperty(name='Preferences Switch', description='', items=[('Render Settings', 'Render Settings', '', 0, 0), ('View Layer Settings', 'View Layer Settings', '', 0, 1)])
    bpy.types.Scene.sna_show_override = bpy.props.BoolProperty(name='Show Override', description='Show Override In Render Context Menu', default=True)
    bpy.types.Scene.sna_show_file_extensions = bpy.props.BoolProperty(name='Show File Extensions', description='Show File Extensions In Render Context Menu', default=True)
    bpy.types.Scene.sna_show_cache_result = bpy.props.BoolProperty(name='Show Cache Result', description='Show Cache Result In Render Context Menu', default=True)
    bpy.types.Scene.sna_show_placeholders = bpy.props.BoolProperty(name='Show Placeholders', description='Show Placeholders In Render Context Menu', default=True)
    bpy.types.Scene.sna_show_file_format = bpy.props.BoolProperty(name='Show File Format', description='Show File Format In Render Context Menu', default=True)
    bpy.types.Scene.sna_show_compression = bpy.props.BoolProperty(name='Show Compression', description='Show Compression In Render Context Menu', default=True)
    bpy.types.Scene.sna_show_render_camera = bpy.props.BoolProperty(name='Show Render Camera', description='Show Render Camera In Render Context Menu', default=True)
    bpy.types.Scene.sna_show_render_engine = bpy.props.BoolProperty(name='Show Render Engine', description='Show Render Engine In Renderer Context Menu', default=True)
    bpy.types.Scene.sna_show_device = bpy.props.BoolProperty(name='Show Device', description='Show Device In Render Engineender Context Menu', default=True)
    bpy.types.Scene.sna_show_samples_cycles = bpy.props.BoolProperty(name='Show Samples Cycles', description='Show Samples(Cycles) In Renderer Context Menu', default=True)
    bpy.types.Scene.sna_show_samples_eevee = bpy.props.BoolProperty(name='Show Samples Eevee', description='Show Samples(Eevee) In Renderer Context Menu', default=True)
    bpy.types.Scene.sna_show_resolutionx = bpy.props.BoolProperty(name='Show Resolution(X)', description='Show Resolution(X) In Renderer Context Menu', default=True)
    bpy.types.Scene.sna_show_resolutiony = bpy.props.BoolProperty(name='Show Resolution(Y)', description='Show Resolution(Y) In Renderer Context Menu', default=True)
    bpy.app.handlers.render_cancel.append(render_cancel_handler_3502C)
    bpy.app.handlers.render_complete.append(render_complete_handler_5EDA9)
    bpy.app.handlers.render_init.append(render_init_handler_59A06)
    bpy.types.TOPBAR_MT_render.append(sna_add_to_topbar_mt_render_8EA94)
    bpy.utils.register_class(SNA_OT_Batcher__Renderer_9Fee1)
    bpy.utils.register_class(SNA_OT_Batcher__View_Layer_Properties_F0859)
    bpy.utils.register_class(SNA_OT_Batcher__Check_For_Updates_2Fa96)
    bpy.utils.register_class(SNA_AddonPreferences_634F4)
    bpy.utils.register_class(SNA_OT_Batcher__Switch_Operator_3F4Fa)
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='Window', space_type='EMPTY')
    kmi = km.keymap_items.new('sna.batcher__renderer_9fee1', 'R', 'PRESS',
        ctrl=True, alt=True, shift=False, repeat=False)
    addon_keymaps['999EA'] = (km, kmi)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_show_resolutiony
    del bpy.types.Scene.sna_show_resolutionx
    del bpy.types.Scene.sna_show_samples_eevee
    del bpy.types.Scene.sna_show_samples_cycles
    del bpy.types.Scene.sna_show_device
    del bpy.types.Scene.sna_show_render_engine
    del bpy.types.Scene.sna_show_render_camera
    del bpy.types.Scene.sna_show_compression
    del bpy.types.Scene.sna_show_file_format
    del bpy.types.Scene.sna_show_placeholders
    del bpy.types.Scene.sna_show_cache_result
    del bpy.types.Scene.sna_show_file_extensions
    del bpy.types.Scene.sna_show_override
    del bpy.types.Scene.sna_preferences_switch
    del bpy.types.Scene.sna_output_image
    del bpy.types.Scene.sna_text_file_path
    del bpy.types.Scene.sna_telegram_chat_id
    bpy.app.handlers.render_cancel.remove(render_cancel_handler_3502C)
    bpy.app.handlers.render_complete.remove(render_complete_handler_5EDA9)
    bpy.app.handlers.render_init.remove(render_init_handler_59A06)
    bpy.types.TOPBAR_MT_render.remove(sna_add_to_topbar_mt_render_8EA94)
    bpy.utils.unregister_class(SNA_OT_Batcher__Renderer_9Fee1)
    bpy.utils.unregister_class(SNA_OT_Batcher__View_Layer_Properties_F0859)
    bpy.utils.unregister_class(SNA_OT_Batcher__Check_For_Updates_2Fa96)
    bpy.utils.unregister_class(SNA_AddonPreferences_634F4)
    bpy.utils.unregister_class(SNA_OT_Batcher__Switch_Operator_3F4Fa)

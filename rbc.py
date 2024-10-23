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
    "name" : "RBC Addon Pro",
    "author" : "AKA Studios", 
    "description" : "",
    "blender" : (3, 0, 0),
    "version" : (1, 3, 2),
    "location" : "View3D>Sidebar>RBC",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "3D View" 
}


import bpy
import bpy.utils.previews
import os
from bpy.app.handlers import persistent
import math
import subprocess
import blf
import mathutils
from bpy.props import BoolProperty, FloatVectorProperty
from bpy_extras import object_utils
import random


addon_keymaps = {}
_icons = None
get_rig_properties = {'sna_wheels': [], 'sna_vehicle_body_axles': [], 'sna_active_motor_constraints': [], 'sna_rb_models_list': [], 'sna_wheels_rb': [], 'sna_new_variable': 0.0, 'sna_vehicle_bodies': [], }
rbc_add_rig_interface = {'sna_enable_list': [], 'sna_compare_list': [], }
rbc_add_rig_quickrig = {'sna_car_body': None, 'sna_wheel_1': [], 'sna_wheel_2': [], 'sna_wheel_model_1': None, 'sna_front_wheel': None, 'sna_wheel_model_2': None, 'sna_car_bodies': [], 'sna_wheels': [], 'sna_axle_pair': [], 'sna_dim': [], 'sna_compare_list': [], }
rbc_animation_funcs = {'sna_rb_obj_list': [], }
rbc_animation_interface = {'sna_rbw_info': '', 'sna_prev_frame': 0, }
rbc_asset_library = {'sna_transer_rbc_rig_props_list': [], 'sna_overlapping_rigs': [], }
rbc_rig_collection = {'sna_unregistered_rig_collection_list': [], 'sna_unregistered_rig_collection_asset_list': [], 'sna_refresh_asset_collection_list': [], 'sna_asset_rig_collection_list': [], 'sna_name': '', }
rbc_rig_controls_funcs = {'sna_speed': 50.75, 'sna_slowmo': 0.5, }
rbc_rig_set_up_funcs = {'sna_rb_model': None, 'sna_collection': None, 'sna_constraint_delete_list': [], 'sna_rig_obj_list': [], }
rbc_rig_tuning_preview_funcs = {'sna_active_axle': None, }
rbc_rig_tuning_funcs = {'sna_body_weight': 0.0, 'sna_bed_weight': 0.0, 'sna_trailer_weight': 0.0, }
rbc_rig_driver_functions = {'sna_active_constraint_list': [], 'sna_value': 0.0, 'sna_target_speed': 0.0, 'sna_points': [], 'sna_acceleration': 0.0, 'sna_frame': 0, 'sna_active_steering_constraint_list': [], }
rbc_rig_interface = {'sna_new_variable': [], }
rbc_scenecollections = {'sna_rbc_collection': None, 'sna_active_obj': None, }
rigging_constraints = {'sna_rbc_wheel': None, }
rigging_parts = {'sna_delete_list': [], 'sna_rbc_list': [], 'sna_remove_from_collection_list': [], 'sna_control_rig': None, 'sna_new_variable': None, 'sna_axles': [], 'sna_car_body': None, 'sna_wheelcambertilt': None, 'sna_wheelbrakecaliper': None, 'sna_wheelrb': None, 'sna_wheelconstraint': None, 'sna_wheelsteeringmotor': None, 'sna_wheelmotor': None, 'sna_hitch_constraint': None, }
rigid_body_tools = {'sna_obj_1': None, 'sna_obj_2': None, }
set_up_generate_rig = {'sna_clear_constraints_list': [], 'sna_lowest_wheel_list': [], }
set_up_generate_rig_convex_hull = {'sna_subobj': None, 'sna_set_empty': None, }
_item_map = dict()


def sna_update_sna_rbc_rig_type_menu_D497D(self, context):
    sna_updated_prop = self.sna_rbc_rig_type_menu
    if sna_updated_prop == "Motorcycle":
        sna_custom_menu_set_B1CFB(1, False, 1, 0, 0, 0, 0)
    elif sna_updated_prop == "Car":
        sna_custom_menu_set_B1CFB(2, False, 2, 0, 0, 0, 0)
    elif sna_updated_prop == "Semi-Truck":
        sna_custom_menu_set_B1CFB(2, False, 2, 1, 2, 1, 2)
    elif sna_updated_prop == "Custom":
        sna_custom_menu_set_B1CFB(2, False, 2, 0, 2, 0, 2)
    elif sna_updated_prop == "Truck":
        sna_custom_menu_set_B1CFB(2, True, 2, 0, 2, 0, 2)
    else:
        pass


def sna_update_enable_breakable_35B13(self, context):
    sna_updated_prop = self.enable_breakable
    sna_breakable_8997A(sna_updated_prop)


def sna_update_enable_anim_constraint_71574(self, context):
    sna_updated_prop = self.enable_anim_constraint
    if sna_updated_prop:
        sna_enable_constraint_EA6A7(True)
        sna_enable_kinematic_5DF45(True)
        sna_disable_drivesteering_5F9C7(True)
    else:
        sna_enable_constraint_EA6A7(False)
        sna_enable_kinematic_5DF45(True)
        sna_disable_drivesteering_5F9C7(False)


def sna_update_breakable_threshold_37669(self, context):
    sna_updated_prop = self.breakable_threshold
    sna_break_threshold_D598F(sna_updated_prop)


def sna_update_record_keyframes_1615C(self, context):
    sna_updated_prop = self.record_keyframes
    if sna_updated_prop:
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.enable_anim_constraint = False
    else:
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.enable_anim_constraint = True


_item_map = dict()


def make_enum_item(_id, name, descr, preview_id, uid):
    lookup = str(_id)+"\0"+str(name)+"\0"+str(descr)+"\0"+str(preview_id)+"\0"+str(uid)
    if not lookup in _item_map:
        _item_map[lookup] = (_id, name, descr, preview_id, uid)
    return _item_map[lookup]


def sna_update_hide_rig_1C4DE(self, context):
    sna_updated_prop = self.hide_rig
    for i_11288 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection)):
        if sna_updated_prop:
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_11288].obj.hide_set(state=True, )
            sna_disable_ray_visablilty_B5A59(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_11288].obj, False)
        else:
            if ('.RB' in bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_11288].obj.name or '.RigControl' in bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_11288].obj.name):
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_11288].obj.hide_set(state=False, )
                sna_disable_ray_visablilty_B5A59(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_11288].obj, False)


def sna_update_sna_active_rig_9D8DD(self, context):
    sna_updated_prop = self.sna_active_rig


def sna_update_sna_rbc_collection_list_7F28B(self, context):
    sna_updated_prop = self.sna_rbc_collection_list
    bpy.context.scene.sna_active_rig = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_rbc_collection_list].name
    sna_rig_auto_select_55240()
    sna_set_camera_C716A()


def sna_update_rig_name_080C1(self, context):
    sna_updated_prop = self.rig_name
    if bpy.context.scene.sna_rename_rig:
        sna_rename_duplicate_names_DDA57(sna_updated_prop)
        self.rig_guide_control.name = sna_updated_prop
        self.rig_drivers.name = sna_updated_prop
        self.rig_collection.name = 'RBC ' + sna_updated_prop + ' Rig'
        self.rig_collection.sna_rbc_asset_collection_properties.name = sna_updated_prop
        for i_0CD76 in range(len(self.rig_obj_collection)):
            if (self.rig_obj_collection[i_0CD76].obj != None):
                self.rig_obj_collection[i_0CD76].obj.name = self.rig_obj_collection[i_0CD76].obj.name.replace(self.name, sna_updated_prop)
        self.name = sna_updated_prop
        bpy.context.scene.sna_active_rig = sna_updated_prop


def sna_update_enable_guide_918E0(self, context):
    sna_updated_prop = self.enable_guide
    if sna_updated_prop:
        pass
    else:
        bpy.ops.sna.drive_reset_d354c('INVOKE_DEFAULT', )
        bpy.ops.sna.steering_reset_ae4f6('INVOKE_DEFAULT', )


def sna_update_disable_steering_7C4F0(self, context):
    sna_updated_prop = self.disable_steering
    for i_90BA2 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if ('Steering' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_90BA2].axle_type and (not 'Differential Steering' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_90BA2].axle_type)):
            for i_B5049 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_90BA2].axle_wheels)):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_90BA2].axle_wheels[i_B5049].wheel_steeringmotor.rigid_body_constraint.enabled = (not sna_updated_prop)


def sna_update_disable_drive_D2572(self, context):
    sna_updated_prop = self.disable_drive
    for i_580EE in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if ('Drive' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_580EE].axle_type or 'Differential' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_580EE].axle_type):
            for i_A809E in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_580EE].axle_wheels)):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_580EE].axle_wheels[i_A809E].wheel_motor.rigid_body_constraint.enabled = (not sna_updated_prop)


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def region_by_type(area, region_type):
    for region in area.regions:
        if region.type == region_type:
            return region
    return area.regions[0]


def sna_update_sna_rig_control_panel_3F2AD(self, context):
    sna_updated_prop = self.sna_rig_control_panel
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.enable_guide = (sna_updated_prop == 'Guides')


def sna_update_wheel_collection_AF401(self, context):
    sna_updated_prop = self.wheel_collection
    if (sna_updated_prop == None):
        if (self.wheel_boundingbox == None):
            pass
        else:
            bpy.data.meshes.remove(mesh=self.wheel_boundingbox.data, )
        self.wheel_button = False
    else:
        if (self.wheel_boundingbox == None):
            pass
        else:
            bpy.data.meshes.remove(mesh=self.wheel_boundingbox.data, )
    if (sna_updated_prop == None):
        pass
    else:
        bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
        for i_9042B in range(len(sna_updated_prop.objects)):
            if sna_updated_prop.objects[i_9042B].type == 'MESH':
                sna_updated_prop.objects[i_9042B].select_set(state=True, )
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
        import bmesh
        import mathutils
        # from blender templates

        def add_box(width, height, depth):
            """
            This function takes inputs and returns vertex and face arrays.
            no actual mesh data creation is done here.
            """
            verts = [(+1.0, +1.0, -1.0),
                     (+1.0, -1.0, -1.0),
                     (-1.0, -1.0, -1.0),
                     (-1.0, +1.0, -1.0),
                     (+1.0, +1.0, +1.0),
                     (+1.0, -1.0, +1.0),
                     (-1.0, -1.0, +1.0),
                     (-1.0, +1.0, +1.0),
                     ]
            faces = [(0, 1, 2, 3),
                     (4, 7, 6, 5),
                     (0, 4, 5, 1),
                     (1, 5, 6, 2),
                     (2, 6, 7, 3),
                     (4, 0, 3, 7),
                    ]
            # apply size
            for i, v in enumerate(verts):
                verts[i] = v[0] * width, v[1] * depth, v[2] * height
            return verts, faces

        def group_bounding_box():
            minx, miny, minz = (999999.0,)*3
            maxx, maxy, maxz = (-999999.0,)*3
            location = [0.0,]*3
            for obj in bpy.context.selected_objects:
                for v in obj.bound_box:
                    v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))
                    if v_world[0] < minx:
                        minx = v_world[0]
                    if v_world[0] > maxx:
                        maxx = v_world[0]
                    if v_world[1] < miny:
                        miny = v_world[1]
                    if v_world[1] > maxy:
                        maxy = v_world[1]
                    if v_world[2] < minz:
                        minz = v_world[2]
                    if v_world[2] > maxz:
                        maxz = v_world[2]
            verts_loc, faces = add_box((maxx-minx)/2, (maxz-minz)/2, (maxy-miny)/2)
            mesh = bpy.data.meshes.new("BoundingBox")
            bm = bmesh.new()
            for v_co in verts_loc:
                bm.verts.new(v_co)
            bm.verts.ensure_lookup_table()
            for f_idx in faces:
                bm.faces.new([bm.verts[i] for i in f_idx])
            bm.to_mesh(mesh)
            mesh.update()
            location[0] = minx+((maxx-minx)/2)
            location[1] = miny+((maxy-miny)/2)
            location[2] = minz+((maxz-minz)/2)
            bbox = object_utils.object_data_add(bpy.context, mesh, operator=None)
            # does a bounding box need to display more than the bounds??
            bbox.location = location
            bbox.display_type = 'BOUNDS'
            bbox.hide_render = True
        group_bounding_box()
        self.wheel_button = True
        self.wheel_boundingbox = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active.name = self.wheel_rb.name + '_BoundBox'
        sna_add_to_rig_obj_collection_31032()
        sna_link_obj_B65F4(bpy.context.view_layer.objects.active, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection)
        sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
        sna_apply_transform_B3258(self.wheel_rb)


def sna_update_body_hitch_button_51522(self, context):
    sna_updated_prop = self.body_hitch_button
    bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
    bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
    if sna_updated_prop:
        sna_hide_obj_select_71598(self.body_hitch_obj, False, False, False, False)
        self.body_hitch_obj.select_set(state=True, )
        bpy.context.view_layer.objects.active = self.body_hitch_obj
        self.body_hitch_obj.show_in_front = True
    else:
        sna_hide_obj_select_71598(self.body_hitch_obj, True, False, False, False)
        self.body_hitch_obj.select_set(state=False, )
        self.body_hitch_obj.show_in_front = False
    sna_lock_axis_2B322(self.body_hitch_obj, sna_updated_prop, self.body_model)


def sna_update_wheel_extra_button_926C2(self, context):
    sna_updated_prop = self.wheel_extra_button
    sna_delete_rbc_constraint_E603C()
    for i_3369C in range(len(bpy.context.view_layer.objects.selected)):
        sna_add_to_rbc_model_collection_CBFB5(bpy.context.view_layer.objects.selected[i_3369C])
        if sna_updated_prop:
            if property_exists("bpy.context.view_layer.objects.selected[i_3369C].constraints['RBC Child Of Brake Caliper']", globals(), locals()):
                pass
            else:
                constraint_D899D = bpy.context.view_layer.objects.selected[i_3369C].constraints.new(type='CHILD_OF', )
                constraint_D899D.name = 'RBC Child Of Brake Caliper'
                constraint_D899D.target = self.wheel_brakecaliper_obj
        else:
            sna_clear_rbc_constraints_0AE2C(bpy.context.view_layer.objects.selected[i_3369C])


def sna_update_wheel_button_CA318(self, context):
    sna_updated_prop = self.wheel_button
    if sna_updated_prop:
        sna_checkdisable_buttons_D6DD2()
        sna_set_rbc_wheel_E46D2(self)
    else:
        sna_reset_rb_any_wheel_23FEE(self)


def sna_update_body_button_846FC(self, context):
    sna_updated_prop = self.body_button
    if bpy.context.scene.sna_transfer_rig_props:
        pass
    else:
        if sna_updated_prop:
            sna_checkdisable_buttons_D6DD2()
            self.body_model = bpy.context.view_layer.objects.active
            sna_obj_type_2568F(self.body_rb, True, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj)
            sna_apply_transform_B3258(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj)
            sna_apply_transform_B3258(self.body_rb)
            bpy.context.view_layer.objects.active = self.body_model
        else:
            self.body_model = None
            sna_reset_car_body_and_rig_76DCC(self.body_rb, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj)


def sna_update_body_collection_FC79B(self, context):
    sna_updated_prop = self.body_collection
    if bpy.context.scene.sna_transfer_rig_props:
        pass
    else:
        if (sna_updated_prop == None):
            if (self.body_boundingbox == None):
                pass
            else:
                bpy.data.meshes.remove(mesh=self.body_boundingbox.data, )
            self.body_button = False
        else:
            if (self.body_boundingbox == None):
                pass
            else:
                bpy.data.meshes.remove(mesh=self.body_boundingbox.data, )
        if (not (sna_updated_prop == None)):
            sna_car_body_collection_A92C7(self.body_rb, sna_updated_prop, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj, self)


def sna_update_body_tuning_button_21E68(self, context):
    sna_updated_prop = self.body_tuning_button
    sna_deselect_body_buttons_01329(sna_updated_prop, self, 'Individual' in bpy.context.scene.sna_rig_tuning_menu.preview_selection)
    if (None != sna_check_bodies_A53C2()):
        pass
    else:
        self.body_tuning_button = True


def sna_update_axle_tuning_button_9E7A2(self, context):
    sna_updated_prop = self.axle_tuning_button
    sna_deselect_axle_buttons_D7FAA(sna_updated_prop, self, 'Individual' in bpy.context.scene.sna_rig_tuning_menu.preview_selection)
    if (None != sna_check_axles_639EB()):
        pass
    else:
        self.axle_tuning_button = True
    sna_show_pivot_points_select_75D30(bpy.context.scene.sna_rig_tuning_menu.show_pivot_points)


def sna_update_preview_selection_0853C(self, context):
    sna_updated_prop = self.preview_selection
    if sna_updated_prop == "Select All":
        sna_activate_all_DF607(True)
    elif sna_updated_prop == "Individual":
        sna_activate_all_DF607(False)
    else:
        pass
    if (sna_check_all_FE38D() != None):
        pass
    else:
        sna_deselect_body_buttons_01329(False, self, True)


def load_preview_icon(path):
    global _icons
    if not path in _icons:
        if os.path.exists(path):
            _icons.load(path, path, "IMAGE")
        else:
            return 0
    return _icons[path].icon_id


def sna_update_physics_weight_position_button_115B6(self, context):
    sna_updated_prop = self.physics_weight_position_button
    bpy.ops.screen.animation_cancel('INVOKE_DEFAULT', )
    bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
    for i_767D4 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_767D4].body_tuning_button:
            if sna_updated_prop:
                sna_weight_position_enabledisable_85D61(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_767D4].body_rb, True, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_767D4].body_model)
                sna_weight_position_lock_axis_4B08F(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_767D4].body_rb, True)
            else:
                sna_weight_position_enabledisable_85D61(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_767D4].body_rb, False, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_767D4].body_model)
                sna_weight_position_lock_axis_4B08F(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_767D4].body_rb, False)


def sna_update_sna_rbc_ground_plane_27EFD(self, context):
    sna_updated_prop = self.sna_rbc_ground_plane
    if property_exists("sna_get_rig_bodywheel_list_188BE(None)[1][0]", globals(), locals()):
        for i_FF842 in range(len(sna_get_rig_bodywheel_list_188BE(None)[1])):
            sna_get_rig_bodywheel_list_188BE(None)[1][i_FF842].physics_roll_constraint.rigid_body_constraint.object1 = sna_updated_prop


def property_exists(prop_path, glob, loc):
    try:
        eval(prop_path, glob, loc)
        return True
    except:
        return False


def sna_update_reverse_drive_BF189(self, context):
    sna_updated_prop = self.reverse_drive
    sna_reverse_drive_C54EC(self, sna_updated_prop)


def sna_update_reverse_steering_A063A(self, context):
    sna_updated_prop = self.reverse_steering
    sna_reverse_steering_38EFC(self, sna_updated_prop)


def sna_update_wheels_pivot_points_AFAE3(self, context):
    sna_updated_prop = self.wheels_pivot_points
    for i_A037B in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].rig_tuning_group.wheels_pivot_points == sna_updated_prop):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].axle_tuning_button:
                for i_F952A in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].axle_wheels)):
                    if 'L' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].axle_wheels[i_F952A].wheel_constraint.name:
                        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].axle_wheels[i_F952A].wheel_constraint.location = (sna_updated_prop, 0.0, 0.0)
                    else:
                        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].axle_wheels[i_F952A].wheel_constraint.location = (float(sna_updated_prop * -1.0), 0.0, 0.0)
        else:
            if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].axle_tuning_button and (bpy.context.scene.sna_rig_tuning_menu.preview_selection == 'Select All')):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_A037B].rig_tuning_group.wheels_pivot_points = sna_updated_prop


def sna_update_wheels_turn_radius_57316(self, context):
    sna_updated_prop = self.wheels_turn_radius
    for i_C48C3 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if ('Steering' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_C48C3].axle_type and (not 'Differential' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_C48C3].axle_type)):
            for i_7A3A3 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_C48C3].axle_wheels)):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_C48C3].axle_wheels[i_7A3A3].wheel_constraint.rigid_body_constraint.limit_ang_z_upper = sna_updated_prop
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_C48C3].axle_wheels[i_7A3A3].wheel_constraint.rigid_body_constraint.limit_ang_z_lower = float(sna_updated_prop * -1.0)


def sna_update_suspension_limits_19909(self, context):
    sna_updated_prop = self.suspension_limits
    for i_143BF in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_143BF].rig_tuning_group.suspension_limits == sna_updated_prop):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_143BF].axle_tuning_button:
                for i_54CCA in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_143BF].axle_wheels)):
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_143BF].axle_wheels[i_54CCA].wheel_constraint.rigid_body_constraint.limit_lin_z_lower = float(float(float(float(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][0].wheel_rb.dimensions[1] / 2.0) * sna_updated_prop) / 4.0) * -1.0)
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_143BF].axle_wheels[i_54CCA].wheel_constraint.rigid_body_constraint.limit_lin_z_upper = float(float(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][0].wheel_rb.dimensions[1] / 2.0) * sna_updated_prop)
        else:
            if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_143BF].axle_tuning_button and (bpy.context.scene.sna_rig_tuning_menu.preview_selection == 'Select All')):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_143BF].rig_tuning_group.suspension_limits = sna_updated_prop


def sna_update_suspension_damping_1BB2D(self, context):
    sna_updated_prop = self.suspension_damping
    for i_9B280 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_9B280].rig_tuning_group.suspension_damping == sna_updated_prop):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_9B280].axle_tuning_button:
                for i_7987B in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_9B280].axle_wheels)):
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_9B280].axle_wheels[i_7987B].wheel_constraint.rigid_body_constraint.spring_damping_z = float(sna_updated_prop * sna_get_vehicle_weight_925DA())
        else:
            if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_9B280].axle_tuning_button and (bpy.context.scene.sna_rig_tuning_menu.preview_selection == 'Select All')):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_9B280].rig_tuning_group.suspension_damping = sna_updated_prop


def sna_update_show_pivot_points_3B8A1(self, context):
    sna_updated_prop = self.show_pivot_points
    sna_show_pivot_points_select_75D30(sna_updated_prop)


def sna_update_suspension_stiffness_5FF25(self, context):
    sna_updated_prop = self.suspension_stiffness
    for i_7F148 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_7F148].rig_tuning_group.suspension_stiffness == sna_updated_prop):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_7F148].axle_tuning_button:
                for i_21EB5 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_7F148].axle_wheels)):
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_7F148].axle_wheels[i_21EB5].wheel_constraint.rigid_body_constraint.spring_stiffness_z = float(sna_updated_prop * sna_get_vehicle_weight_925DA())
        else:
            if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_7F148].axle_tuning_button and (bpy.context.scene.sna_rig_tuning_menu.preview_selection == 'Select All')):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_7F148].rig_tuning_group.suspension_stiffness = sna_updated_prop


def sna_update_physics_weight_E6ACC(self, context):
    sna_updated_prop = self.physics_weight
    for i_2D0D3 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_tuning_button:
            sna_set_weight_E58E3(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb, sna_updated_prop)
    for i_83D3B in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb.sna_body_axles)):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb.sna_body_axles[i_83D3B].rig_tuning_group.suspension_stiffness = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb.sna_body_axles[i_83D3B].rig_tuning_group.suspension_stiffness
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb.sna_body_axles[i_83D3B].rig_tuning_group.suspension_damping = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb.sna_body_axles[i_83D3B].rig_tuning_group.suspension_damping
        for i_1B879 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb.sna_body_axles[i_83D3B].axle_wheels)):
            sna_set_weight_E58E3(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_2D0D3].body_rb.sna_body_axles[i_83D3B].axle_wheels[i_1B879].wheel_rb, sna_updated_prop)


def sna_update_physics_tire_friction_E904C(self, context):
    sna_updated_prop = self.physics_tire_friction
    for i_95BD5 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if (sna_updated_prop == sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_95BD5].rig_tuning_group.physics_tire_friction):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_95BD5].axle_tuning_button:
                for i_44E1C in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_95BD5].axle_wheels)):
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_95BD5].axle_wheels[i_44E1C].wheel_rb.rigid_body.friction = sna_updated_prop
        else:
            if ((bpy.context.scene.sna_rig_tuning_menu.preview_selection == 'Select All') and sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_95BD5].axle_tuning_button):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_95BD5].rig_tuning_group.physics_tire_friction = sna_updated_prop


def sna_update_drive_type_7DA4C(self, context):
    sna_updated_prop = self.drive_type
    if bpy.context.scene.sna_transfer_rig_props:
        pass
    else:
        for i_49EAD in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_updated_prop == "2WD":
                sna_drive_type_175F5(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_49EAD], i_49EAD, 'Steering', 'Drive')
            elif sna_updated_prop == "4WD":
                sna_drive_type_175F5(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_49EAD], i_49EAD, 'Drive + Steering', 'Drive')
            elif sna_updated_prop == "FWD":
                sna_drive_type_175F5(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_49EAD], i_49EAD, 'Drive + Steering', 'Dead')
            elif sna_updated_prop == "DSD":
                sna_drive_type_175F5(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_49EAD], i_49EAD, 'Differential Steering', 'Differential Steering')
            elif sna_updated_prop == "RWS":
                sna_drive_type_175F5(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_49EAD], i_49EAD, 'Drive', 'Steering')
            elif sna_updated_prop == "FWS+RWS":
                sna_drive_type_175F5(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_49EAD], i_49EAD, 'Drive + Steering', 'Drive + Steering')
            else:
                pass


def sna_update_wheels_camber_angle_DE85F(self, context):
    sna_updated_prop = self.wheels_camber_angle
    for i_8A465 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].rig_tuning_group.wheels_camber_angle == sna_updated_prop):
            if (sna_updated_prop == 0.0):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_wheels[1].wheel_model.constraints['RBC Camber Tilt'].use_y = False
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_wheels[0].wheel_model.constraints['RBC Camber Tilt'].use_y = False
            else:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_wheels[1].wheel_model.constraints['RBC Camber Tilt'].use_y = True
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_wheels[0].wheel_model.constraints['RBC Camber Tilt'].use_y = True
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_wheels[1].wheel_cambertilt_obj.rotation_euler = (0.0, sna_updated_prop, 0.0)
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_wheels[0].wheel_cambertilt_obj.rotation_euler = (0.0, float(sna_updated_prop * -1.0), 0.0)
        else:
            if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].axle_tuning_button and (bpy.context.scene.sna_rig_tuning_menu.preview_selection == 'Select All')):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8A465].rig_tuning_group.wheels_camber_angle = sna_updated_prop


def sna_update_physics_roll_constraint_button_C7BCE(self, context):
    sna_updated_prop = self.physics_roll_constraint_button
    if sna_updated_prop:
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        self.physics_roll_constraint.rigid_body_constraint.enabled = True
    else:
        self.physics_roll_constraint.rigid_body_constraint.enabled = False


def sna_update_physics_roll_constraint_x_angle_F95D6(self, context):
    sna_updated_prop = self.physics_roll_constraint_x_angle
    self.physics_roll_constraint.rigid_body_constraint.limit_ang_x_lower = float(sna_updated_prop * -1.0)
    self.physics_roll_constraint.rigid_body_constraint.limit_ang_x_upper = sna_updated_prop


def sna_update_physics_roll_constraint_y_angle_27A57(self, context):
    sna_updated_prop = self.physics_roll_constraint_y_angle
    self.physics_roll_constraint.rigid_body_constraint.limit_ang_y_lower = float(sna_updated_prop * -1.0)
    self.physics_roll_constraint.rigid_body_constraint.limit_ang_y_upper = sna_updated_prop


def sna_update_axle_type_3DB7C(self, context):
    sna_updated_prop = self.axle_type
    for i_A57AE in range(len(self.axle_wheels)):
        if sna_updated_prop == "Drive":
            sna_update_wheel_C1773(self.axle_wheels[i_A57AE], False, True, self.rig_tuning_group.wheels_turn_radius)
        elif sna_updated_prop == "Steering":
            sna_update_wheel_C1773(self.axle_wheels[i_A57AE], True, False, self.rig_tuning_group.wheels_turn_radius)
        elif sna_updated_prop == "Drive + Steering":
            sna_update_wheel_C1773(self.axle_wheels[i_A57AE], True, True, self.rig_tuning_group.wheels_turn_radius)
        elif sna_updated_prop == "Dead":
            sna_update_wheel_C1773(self.axle_wheels[i_A57AE], False, False, self.rig_tuning_group.wheels_turn_radius)
        elif sna_updated_prop == "Differential Steering":
            sna_update_wheel_C1773(self.axle_wheels[i_A57AE], False, True, self.rig_tuning_group.wheels_turn_radius)
        else:
            pass


def sna_update_sna_rbc_rig_panel_F8101(self, context):
    sna_updated_prop = self.sna_rbc_rig_panel
    bpy.context.scene.sna_rig_tuning_menu.preview_selection = bpy.context.scene.sna_rig_tuning_menu.preview_selection
    if (len(list(bpy.context.scene.sna_rig_tuning_enum)) == 0):
        bpy.context.scene.sna_rig_tuning_enum = set(['Wheels'])


def sna_update_performance_9CF7A(self, context):
    sna_updated_prop = self.performance
    if sna_updated_prop == "Low":
        sna_rbc_body_collision_type_ADADE('CONVEX_HULL')
        bpy.context.scene.rigidbody_world.substeps_per_frame = 10
        bpy.context.scene.rigidbody_world.solver_iterations = 25
    elif sna_updated_prop == "Medium":
        sna_rbc_body_collision_type_ADADE('CONVEX_HULL')
        bpy.context.scene.rigidbody_world.substeps_per_frame = 15
        bpy.context.scene.rigidbody_world.solver_iterations = 35
    elif sna_updated_prop == "High":
        sna_rbc_body_collision_type_ADADE('MESH')
        bpy.context.scene.rigidbody_world.substeps_per_frame = 25
        bpy.context.scene.rigidbody_world.solver_iterations = 50
    else:
        pass


def random_integer(min, max, seed):
    random.seed(seed)
    return random.randint(int(min), int(max))


class SNA_OT_Operator_46C07(bpy.types.Operator):
    bl_idname = "sna.operator_46c07"
    bl_label = "Operator"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_DEV_TOOLS_EC795(bpy.types.Panel):
    bl_label = 'Dev Tools'
    bl_idname = 'SNA_PT_DEV_TOOLS_EC795'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (True)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout


class SNA_OT_Dev_Transfer_Props_C5508(bpy.types.Operator):
    bl_idname = "sna.dev_transfer_props_c5508"
    bl_label = "Dev Transfer Props"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_get_rig_bodywheel_list_188BE(Rig_Prop):
    get_rig_properties['sna_vehicle_body_axles'] = []
    get_rig_properties['sna_vehicle_bodies'] = []
    get_rig_properties['sna_wheels'] = []
    get_rig_properties['sna_active_motor_constraints'] = []
    get_rig_properties['sna_rb_models_list'] = []
    for i_380C9 in range(len(Rig_Prop.rig_bodies)):
        get_rig_properties['sna_vehicle_bodies'].append(Rig_Prop.rig_bodies[i_380C9])
        if (Rig_Prop.rig_bodies[i_380C9].body_model == None):
            pass
        else:
            get_rig_properties['sna_rb_models_list'].append(Rig_Prop.rig_bodies[i_380C9].body_model)
        for i_A6107 in range(len(Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles)):
            get_rig_properties['sna_vehicle_body_axles'].append(Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles[i_A6107])
            for i_073C9 in range(len(Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles[i_A6107].axle_wheels)):
                get_rig_properties['sna_wheels'].append(Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles[i_A6107].axle_wheels[i_073C9])
                if (Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles[i_A6107].axle_wheels[i_073C9].wheel_model == None):
                    pass
                else:
                    get_rig_properties['sna_rb_models_list'].append(Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles[i_A6107].axle_wheels[i_073C9].wheel_model)
                get_rig_properties['sna_active_motor_constraints'].append(Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles[i_A6107].axle_wheels[i_073C9].wheel_motor)
    if property_exists("Rig_Prop", globals(), locals()):
        return [get_rig_properties['sna_wheels'], get_rig_properties['sna_vehicle_bodies'], get_rig_properties['sna_vehicle_body_axles'], Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles[i_A6107].axle_wheels, Rig_Prop.rig_bodies, Rig_Prop.rig_bodies[i_380C9].body_rb.sna_body_axles, get_rig_properties['sna_rb_models_list']]


def sna_active_wheel_rb_list_DFE0F():
    get_rig_properties['sna_wheels_rb'] = []
    for i_6BD43 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        get_rig_properties['sna_wheels_rb'].append(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_6BD43].wheel_rb)
    return get_rig_properties['sna_wheels_rb']


def sna_rbc_rig_type_menu_enum_items(self, context):
    enum_items = [['Car', 'Car', '', 37], ['Motorcycle', 'Motorcycle', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Motorcycle_icon.png'))], ['Truck', 'Truck', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Truck_icon.png'))], ['Semi-Truck', 'Semi-Truck', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Semi-Truck_icon.png'))], ['Custom', 'Custom', '', 92], ['Quick Rig', 'Quick Rig', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_QuickRig_Icon.png'))]]
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_rbc_rig_group_rig_type_enum_items(self, context):
    enum_items = [['Car', 'Car', '', 37], ['Motorcycle', 'Motorcycle', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Motorcycle_icon.png'))], ['Truck', 'Truck', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Truck_icon.png'))], ['Semi-Truck', 'Semi-Truck', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Semi-Truck_icon.png'))], ['Custom', 'Custom', '', 92], ['Quick Rig', 'Quick Rig', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_QuickRig_Icon.png'))]]
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_custom_menu_get_E69C0():
    return [bpy.context.scene.sna_custom_vehicle_set.vehicle_front_axle_wheels, bpy.context.scene.sna_custom_vehicle_set.vehicle_bed, bpy.context.scene.sna_custom_vehicle_set.vehicle_back_axle_wheels, bpy.context.scene.sna_custom_vehicle_set.extra_back_axles, bpy.context.scene.sna_custom_vehicle_set.extra_back_axles_wheels, bpy.context.scene.sna_custom_vehicle_set.vehicle_trailer, bpy.context.scene.sna_custom_vehicle_set.vehicle_trailer_axles]


def sna_create_a_rig_C8491(Input, Front_Axle_Wheels, Vehicle_Bed, Back_Axle_Wheels, Extra_Back_Axle, Extra_Back_Axle_Wheels, Trailers, Trailer_Axles):
    bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
    id_0_ecde9, id_name_1_ecde9, prop_2_ecde9 = sna_create_rbc_rig_prop_9B9C6()
    sna_create_rbc_collection_7D211(prop_2_ecde9)
    control_rig_0_66565 = sna_add_rbc_rig_control_5F8F2(id_name_1_ecde9, '.RigControl', prop_2_ecde9)
    vehicle_body_0_e3fde, vehicle_bed_1_e3fde = sna_create_vehicle_body_AD0C5(prop_2_ecde9, Vehicle_Bed, id_name_1_ecde9)
    sna_create_rbc_axle_5CDFD('F', id_name_1_ecde9, Front_Axle_Wheels, 'Steering', vehicle_body_0_e3fde, 1, False)
    sna_create_rbc_axle_5CDFD('B', id_name_1_ecde9, Back_Axle_Wheels, 'Drive', vehicle_bed_1_e3fde, 1, False)
    sna_create_rbc_axle_5CDFD('B2', id_name_1_ecde9, Extra_Back_Axle_Wheels, 'Dead', vehicle_bed_1_e3fde, Extra_Back_Axle, False)
    sna_create_trailer_F4A92(id_name_1_ecde9, prop_2_ecde9, vehicle_bed_1_e3fde, Trailers, Trailer_Axles, 0)
    sna_create_disable_constraints_28638((property_exists("prop_2_ecde9.rig_bodies", globals(), locals()) and len(prop_2_ecde9.rig_bodies) > 1), 0)
    if prop_2_ecde9.rig_type == "Quick Rig":
        prop_2_ecde9.drive_type = '2WD'
    else:
        pass


class SNA_OT_Add_Rig_Type_B03D7(bpy.types.Operator):
    bl_idname = "sna.add_rig_type_b03d7"
    bl_label = "Add Rig Type"
    bl_description = "Adds selected rig type"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        sna_add_rbc_scene_DCE04()
        bpy.context.scene.sna_rename_rig = False
        sna_create_a_rig_C8491(None, sna_custom_menu_get_E69C0()[0], sna_custom_menu_get_E69C0()[1], sna_custom_menu_get_E69C0()[2], sna_custom_menu_get_E69C0()[3], sna_custom_menu_get_E69C0()[4], sna_custom_menu_get_E69C0()[5], sna_custom_menu_get_E69C0()[6])
        bpy.context.scene.sna_rbc_rig_panel = set(['Set Up'])
        bpy.context.scene.sna_rig_tuning_enum = set(['Wheels'])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_custom_menu_set_B1CFB(Front_Axle_Wheels, Vehicle_Bed, Back_Axle_Wheels, Extra_Back_Axle, Extra_Back_Axle_Wheels, Trailers, Trailer_Axles):
    bpy.context.scene.sna_custom_vehicle_set.vehicle_front_axle_wheels = Front_Axle_Wheels
    bpy.context.scene.sna_custom_vehicle_set.vehicle_bed = Vehicle_Bed
    bpy.context.scene.sna_custom_vehicle_set.vehicle_back_axle_wheels = Back_Axle_Wheels
    bpy.context.scene.sna_custom_vehicle_set.extra_back_axles = Extra_Back_Axle
    bpy.context.scene.sna_custom_vehicle_set.extra_back_axles_wheels = Extra_Back_Axle_Wheels
    bpy.context.scene.sna_custom_vehicle_set.vehicle_trailer = Trailers
    bpy.context.scene.sna_custom_vehicle_set.vehicle_trailer_axles = Trailer_Axles


def sna_preview_menu_57DE0(layout_function, front_axle_wheels, vehicle_bed, back_axle_wheels, extra_back_axles, extra_back_axles_wheels, vehicle_trailer, vehicle_trailer_axles):
    layout_function = layout_function
    sna_wheel_button_FB4B1(layout_function, (front_axle_wheels == 2))
    layout_function = layout_function
    sna_car_body_button_preview_E4923(layout_function, vehicle_bed, 'Body')
    layout_function = layout_function
    sna_wheel_button_FB4B1(layout_function, (back_axle_wheels == 2))
    for i_C84F1 in range(extra_back_axles):
        layout_function = layout_function
        sna_wheel_button_FB4B1(layout_function, (extra_back_axles_wheels == 2))
    for i_4FCFA in range(vehicle_trailer):
        layout_function = layout_function
        sna_trailer_icon_preview_3C66B(layout_function, )
    for i_6DB32 in range(vehicle_trailer_axles):
        if (vehicle_trailer == 1):
            layout_function = layout_function
            sna_wheel_button_FB4B1(layout_function, True)


def sna_car_body_button_preview_E4923(layout_function, is_double, name):
    col_066D1 = layout_function.column(heading='', align=False)
    col_066D1.alert = False
    col_066D1.enabled = True
    col_066D1.active = True
    col_066D1.use_property_split = False
    col_066D1.use_property_decorate = False
    col_066D1.scale_x = 1.0
    col_066D1.scale_y = -2.7799997329711914
    col_066D1.alignment = 'Expand'.upper()
    col_066D1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_066D1.label(text='', icon_value=0)
    if is_double:
        col_1054C = layout_function.column(heading='', align=False)
        col_1054C.alert = False
        col_1054C.enabled = True
        col_1054C.active = True
        col_1054C.use_property_split = False
        col_1054C.use_property_decorate = False
        col_1054C.scale_x = 1.0
        col_1054C.scale_y = 1.0
        col_1054C.alignment = 'Expand'.upper()
        col_1054C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_42D57 = col_1054C.column(heading='', align=False)
        col_42D57.alert = False
        col_42D57.enabled = True
        col_42D57.active = True
        col_42D57.use_property_split = False
        col_42D57.use_property_decorate = False
        col_42D57.scale_x = 1.0
        col_42D57.scale_y = -0.559999942779541
        col_42D57.alignment = 'Expand'.upper()
        col_42D57.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_42D57.label(text='', icon_value=0)
        col_1054C.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Bed.png')), scale=4.0)
        col_C4C65 = col_1054C.column(heading='', align=False)
        col_C4C65.alert = False
        col_C4C65.enabled = True
        col_C4C65.active = True
        col_C4C65.use_property_split = False
        col_C4C65.use_property_decorate = False
        col_C4C65.scale_x = 1.0
        col_C4C65.scale_y = -2.419999837875366
        col_C4C65.alignment = 'Expand'.upper()
        col_C4C65.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_C4C65.label(text='', icon_value=0)
        col_1054C.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Bed2.png')), scale=4.0)
        col_1BE3F = col_1054C.column(heading='', align=False)
        col_1BE3F.alert = False
        col_1BE3F.enabled = True
        col_1BE3F.active = True
        col_1BE3F.use_property_split = False
        col_1BE3F.use_property_decorate = False
        col_1BE3F.scale_x = 1.0
        col_1BE3F.scale_y = 0.17999999225139618
        col_1BE3F.alignment = 'Expand'.upper()
        col_1BE3F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_1BE3F.label(text='', icon_value=0)
    else:
        layout_function.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Body.png')), scale=4.0)
        col_644FA = layout_function.column(heading='', align=False)
        col_644FA.alert = False
        col_644FA.enabled = True
        col_644FA.active = True
        col_644FA.use_property_split = False
        col_644FA.use_property_decorate = False
        col_644FA.scale_x = 1.0
        col_644FA.scale_y = 0.6399999260902405
        col_644FA.alignment = 'Expand'.upper()
        col_644FA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_644FA.label(text='', icon_value=0)


def sna_compare_list_49E92(Input):
    rbc_add_rig_interface['sna_compare_list'] = []
    for i_61040 in range(Input):
        rbc_add_rig_interface['sna_compare_list'].append(True)
    return rbc_add_rig_interface['sna_compare_list']


def sna_boolean_list_0588A():
    rbc_add_rig_interface['sna_enable_list'] = []
    for i_49B81 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
        rbc_add_rig_interface['sna_enable_list'].append(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_49B81].body_button)
        for i_35530 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_49B81].body_rb.sna_body_axles)):
            for i_C7A22 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_49B81].body_rb.sna_body_axles[i_35530].axle_wheels)):
                rbc_add_rig_interface['sna_enable_list'].append(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_49B81].body_rb.sna_body_axles[i_35530].axle_wheels[i_C7A22].wheel_button)
    return rbc_add_rig_interface['sna_enable_list']


def sna_enable_generate_button_C50DB():
    return (sna_boolean_list_0588A() == sna_compare_list_49E92(len(sna_boolean_list_0588A())))


def sna_rbc_add_rig_08E47(layout_function, ):
    col_31C47 = layout_function.column(heading='', align=True)
    col_31C47.alert = False
    col_31C47.enabled = True
    col_31C47.active = True
    col_31C47.use_property_split = False
    col_31C47.use_property_decorate = False
    col_31C47.scale_x = 1.0
    col_31C47.scale_y = 1.25
    col_31C47.alignment = 'Expand'.upper()
    col_31C47.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if (bpy.context.scene.sna_rbc_rig_type_menu == 'Quick Rig'):
        op = col_31C47.operator('sna.quick_rig_631dc', text='Quick Rig', icon_value=9, emboss=True, depress=False)
    else:
        op = col_31C47.operator('sna.add_rig_type_b03d7', text='Add Rig', icon_value=9, emboss=True, depress=False)
    col_31C47.prop(bpy.context.scene, 'sna_rbc_rig_type_menu', text='', icon_value=0, emboss=True)
    if (bpy.context.scene.sna_rbc_rig_type_menu == 'Quick Rig'):
        col_94668 = layout_function.column(heading='', align=False)
        col_94668.alert = False
        col_94668.enabled = True
        col_94668.active = True
        col_94668.use_property_split = False
        col_94668.use_property_decorate = False
        col_94668.scale_x = 1.0
        col_94668.scale_y = 1.0
        col_94668.alignment = 'Expand'.upper()
        col_94668.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_94668.prop(bpy.context.scene, 'sna_quick_rig_instructions', text='Quick Rig Instructions(Click Me)', icon_value=2, emboss=False, toggle=False)
        if bpy.context.scene.sna_quick_rig_instructions:
            col_217C4 = col_94668.column(heading='', align=False)
            col_217C4.alert = False
            col_217C4.enabled = True
            col_217C4.active = True
            col_217C4.use_property_split = False
            col_217C4.use_property_decorate = False
            col_217C4.scale_x = 1.0
            col_217C4.scale_y = 1.0
            col_217C4.alignment = 'Expand'.upper()
            col_217C4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_217C4.label(text='-Have at least 3 objects selected', icon_value=0)
            col_217C4.label(text='-Face Vehicle Frontwards', icon_value=0)
            col_217C4.label(text="-Doesn't support empty/collection hierarchy", icon_value=0)
            col_217C4.label(text="-Doesn't support Vehicle Beds or Trailers", icon_value=0)
    else:
        col_DA32D = layout_function.column(heading='', align=True)
        col_DA32D.alert = False
        col_DA32D.enabled = True
        col_DA32D.active = True
        col_DA32D.use_property_split = False
        col_DA32D.use_property_decorate = False
        col_DA32D.scale_x = 1.0
        col_DA32D.scale_y = 1.0
        col_DA32D.alignment = 'Expand'.upper()
        col_DA32D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_7D70C = col_DA32D.split(factor=0.5, align=True)
        split_7D70C.alert = False
        split_7D70C.enabled = True
        split_7D70C.active = True
        split_7D70C.use_property_split = False
        split_7D70C.use_property_decorate = False
        split_7D70C.scale_x = 1.0
        split_7D70C.scale_y = 1.0
        split_7D70C.alignment = 'Expand'.upper()
        if not True: split_7D70C.operator_context = "EXEC_DEFAULT"
        split_7D70C.prop(bpy.context.scene.sna_custom_vehicle_set, 'enable_menu', text='Custom Menu', icon_value=0, emboss=True, toggle=True)
        split_7D70C.prop(bpy.context.scene.sna_custom_vehicle_set, 'enable_preview', text='Preview', icon_value=0, emboss=True, toggle=True)
        if bpy.context.scene.sna_custom_vehicle_set.enable_menu:
            col_5DBBE = col_DA32D.column(heading='', align=True)
            col_5DBBE.alert = False
            col_5DBBE.enabled = True
            col_5DBBE.active = True
            col_5DBBE.use_property_split = False
            col_5DBBE.use_property_decorate = False
            col_5DBBE.scale_x = 1.0
            col_5DBBE.scale_y = 1.0
            col_5DBBE.alignment = 'Expand'.upper()
            col_5DBBE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            box_229AD = col_5DBBE.box()
            box_229AD.alert = False
            box_229AD.enabled = True
            box_229AD.active = True
            box_229AD.use_property_split = False
            box_229AD.use_property_decorate = False
            box_229AD.alignment = 'Expand'.upper()
            box_229AD.scale_x = 1.0
            box_229AD.scale_y = 1.0
            if not True: box_229AD.operator_context = "EXEC_DEFAULT"
            col_A01F3 = box_229AD.column(heading='', align=True)
            col_A01F3.alert = False
            col_A01F3.enabled = True
            col_A01F3.active = True
            col_A01F3.use_property_split = False
            col_A01F3.use_property_decorate = False
            col_A01F3.scale_x = 1.0
            col_A01F3.scale_y = 1.0
            col_A01F3.alignment = 'Expand'.upper()
            col_A01F3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_A01F3.prop(bpy.context.scene.sna_custom_vehicle_set, 'vehicle_front_axle_wheels', text='Front Axle Wheels', icon_value=0, emboss=True, toggle=True)
            col_A01F3.prop(bpy.context.scene.sna_custom_vehicle_set, 'vehicle_back_axle_wheels', text='Back Axle Wheels', icon_value=0, emboss=True, toggle=True)
            col_A01F3.prop(bpy.context.scene.sna_custom_vehicle_set, 'vehicle_bed', text='Vehicle Bed', icon_value=0, emboss=True, toggle=True)
            box_486EB = col_5DBBE.box()
            box_486EB.alert = False
            box_486EB.enabled = True
            box_486EB.active = True
            box_486EB.use_property_split = False
            box_486EB.use_property_decorate = False
            box_486EB.alignment = 'Expand'.upper()
            box_486EB.scale_x = 1.0
            box_486EB.scale_y = 1.0
            if not True: box_486EB.operator_context = "EXEC_DEFAULT"
            col_26C12 = box_486EB.column(heading='', align=True)
            col_26C12.alert = False
            col_26C12.enabled = True
            col_26C12.active = True
            col_26C12.use_property_split = False
            col_26C12.use_property_decorate = False
            col_26C12.scale_x = 1.0
            col_26C12.scale_y = 1.0
            col_26C12.alignment = 'Expand'.upper()
            col_26C12.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_26C12.prop(bpy.context.scene.sna_custom_vehicle_set, 'extra_back_axles', text='Extra Back Axles', icon_value=0, emboss=True, toggle=True)
            col_26C12.prop(bpy.context.scene.sna_custom_vehicle_set, 'extra_back_axles_wheels', text='Extra Back Axles Wheels', icon_value=0, emboss=True, toggle=True)
            box_4B9D9 = col_5DBBE.box()
            box_4B9D9.alert = False
            box_4B9D9.enabled = True
            box_4B9D9.active = True
            box_4B9D9.use_property_split = False
            box_4B9D9.use_property_decorate = False
            box_4B9D9.alignment = 'Expand'.upper()
            box_4B9D9.scale_x = 1.0
            box_4B9D9.scale_y = 1.0
            if not True: box_4B9D9.operator_context = "EXEC_DEFAULT"
            col_F408F = box_4B9D9.column(heading='', align=True)
            col_F408F.alert = False
            col_F408F.enabled = True
            col_F408F.active = True
            col_F408F.use_property_split = False
            col_F408F.use_property_decorate = False
            col_F408F.scale_x = 1.0
            col_F408F.scale_y = 1.0
            col_F408F.alignment = 'Expand'.upper()
            col_F408F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_F408F.prop(bpy.context.scene.sna_custom_vehicle_set, 'vehicle_trailer', text='Trailer', icon_value=0, emboss=True, toggle=True)
            col_F408F.prop(bpy.context.scene.sna_custom_vehicle_set, 'vehicle_trailer_axles', text='Trailer Axles', icon_value=0, emboss=True, toggle=True)
        layout_function = col_DA32D
        sna_preview_3BB91(layout_function, )


def sna_trailer_icon_preview_3C66B(layout_function, ):
    col_FF8F6 = layout_function.column(heading='', align=False)
    col_FF8F6.alert = False
    col_FF8F6.enabled = True
    col_FF8F6.active = True
    col_FF8F6.use_property_split = False
    col_FF8F6.use_property_decorate = False
    col_FF8F6.scale_x = 1.0
    col_FF8F6.scale_y = -2.0
    col_FF8F6.alignment = 'Expand'.upper()
    col_FF8F6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_FF8F6.label(text='', icon_value=0)
    layout_function.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Trailer.png')), scale=4.0)
    layout_function.label(text='', icon_value=0)


def sna_wheel_button_FB4B1(layout_function, is_double):
    col_1C650 = layout_function.column(heading='', align=False)
    col_1C650.alert = False
    col_1C650.enabled = True
    col_1C650.active = True
    col_1C650.use_property_split = False
    col_1C650.use_property_decorate = False
    col_1C650.scale_x = 1.0
    col_1C650.scale_y = -3.7300000190734863
    col_1C650.alignment = 'Expand'.upper()
    col_1C650.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_1C650.label(text='', icon_value=0)
    if is_double:
        layout_function.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Axle.png')), scale=5.0)
    else:
        layout_function.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Single.png')), scale=5.0)


class SNA_PT_RBC_ADD_RIG_FFA05(bpy.types.Panel):
    bl_label = 'RBC Add Rig'
    bl_idname = 'SNA_PT_RBC_ADD_RIG_FFA05'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 1
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=233, scale=1.0)

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_rbc_add_rig_08E47(layout_function, )


def sna_preview_3BB91(layout_function, ):
    col_FA1CA = layout_function.column(heading='', align=True)
    col_FA1CA.alert = False
    col_FA1CA.enabled = True
    col_FA1CA.active = True
    col_FA1CA.use_property_split = False
    col_FA1CA.use_property_decorate = False
    col_FA1CA.scale_x = 1.0
    col_FA1CA.scale_y = 1.0
    col_FA1CA.alignment = 'Expand'.upper()
    col_FA1CA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if bpy.context.scene.sna_custom_vehicle_set.enable_preview:
        box_93653 = col_FA1CA.box()
        box_93653.alert = False
        box_93653.enabled = False
        box_93653.active = True
        box_93653.use_property_split = False
        box_93653.use_property_decorate = False
        box_93653.alignment = 'Expand'.upper()
        box_93653.scale_x = 1.0
        box_93653.scale_y = 1.0
        if not True: box_93653.operator_context = "EXEC_DEFAULT"
        col_8D25A = box_93653.column(heading='', align=False)
        col_8D25A.alert = False
        col_8D25A.enabled = True
        col_8D25A.active = True
        col_8D25A.use_property_split = False
        col_8D25A.use_property_decorate = False
        col_8D25A.scale_x = 1.0
        col_8D25A.scale_y = 1.7799999713897705
        col_8D25A.alignment = 'Expand'.upper()
        col_8D25A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_8D25A.label(text='', icon_value=0)
        layout_function = box_93653
        sna_preview_menu_57DE0(layout_function, sna_custom_menu_get_E69C0()[0], sna_custom_menu_get_E69C0()[1], sna_custom_menu_get_E69C0()[2], sna_custom_menu_get_E69C0()[3], sna_custom_menu_get_E69C0()[4], sna_custom_menu_get_E69C0()[5], sna_custom_menu_get_E69C0()[6])
        col_4D00C = box_93653.column(heading='', align=False)
        col_4D00C.alert = False
        col_4D00C.enabled = True
        col_4D00C.active = True
        col_4D00C.use_property_split = False
        col_4D00C.use_property_decorate = False
        col_4D00C.scale_x = 1.0
        col_4D00C.scale_y = -1.6200000047683716
        col_4D00C.alignment = 'Expand'.upper()
        col_4D00C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_4D00C.label(text='', icon_value=0)


def sna_quickrig_B3110(Input, Axles, Axle_Wheels, Car_Body_2, Axles_2, Axle_Wheels_2):
    bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
    id_0_d1e42, id_name_1_d1e42, prop_2_d1e42 = sna_create_rbc_rig_prop_9B9C6()
    sna_create_rbc_collection_7D211(prop_2_d1e42)
    control_rig_0_6a55f = sna_add_rbc_rig_control_5F8F2(id_name_1_d1e42, '.RigControl', prop_2_d1e42)
    vehicle_body_0_5e0e3, vehicle_bed_1_5e0e3 = sna_create_vehicle_body_AD0C5(prop_2_d1e42, False, id_name_1_d1e42)
    sna_create_rbc_axle_5CDFD('Front', id_name_1_d1e42, 2, 'Dead', vehicle_body_0_5e0e3, Axles, False)
    prop_2_d1e42.drive_type = '2WD'


def sna_find_dim_9A738():
    rbc_add_rig_quickrig['sna_dim'] = []
    for i_DDAC2 in range(len(bpy.context.view_layer.objects.selected)):
        rbc_add_rig_quickrig['sna_dim'].append(round(float(float(bpy.context.view_layer.objects.selected[i_DDAC2].dimensions[0] + bpy.context.view_layer.objects.selected[i_DDAC2].dimensions[1] + bpy.context.view_layer.objects.selected[i_DDAC2].dimensions[2]) / 3.0), abs(1)))
    return None


def sna_assign_carwheels_E2BBF():
    rbc_add_rig_quickrig['sna_car_bodies'] = []
    rbc_add_rig_quickrig['sna_wheels'] = []
    for i_121A1 in range(len(bpy.context.view_layer.objects.selected)):
        if (round(float(float(bpy.context.view_layer.objects.selected[i_121A1].dimensions[0] + bpy.context.view_layer.objects.selected[i_121A1].dimensions[1] + bpy.context.view_layer.objects.selected[i_121A1].dimensions[2]) / 3.0), abs(1)) == round(sorted(rbc_add_rig_quickrig['sna_dim'], reverse=True)[0], abs(1))):
            rbc_add_rig_quickrig['sna_car_bodies'].append(bpy.context.view_layer.objects.selected[i_121A1])
        else:
            rbc_add_rig_quickrig['sna_wheels'].append(bpy.context.view_layer.objects.selected[i_121A1])
        Wheels = rbc_add_rig_quickrig['sna_wheels']
        sorted_objects = None
        # Get the selected objects
        selected_objects = Wheels
        # Sort the selected objects by their x and y coordinates
        sorted_objects = sorted(selected_objects, key=lambda obj: (round(obj.location.y, 1), round(obj.location.x, 1)))
        rbc_add_rig_quickrig['sna_wheels'] = sorted_objects


class SNA_OT_Quick_Rig_Set__Aa043(bpy.types.Operator):
    bl_idname = "sna.quick_rig_set__aa043"
    bl_label = "Quick Rig Set "
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_1A5CE in range(len(rbc_add_rig_quickrig['sna_car_bodies'])):
            rbc_add_rig_quickrig['sna_car_bodies'][i_1A5CE].select_set(state=True, )
            bpy.context.view_layer.objects.active = rbc_add_rig_quickrig['sna_car_bodies'][i_1A5CE]
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][0].body_button = True
        for i_C1E93 in range(len(rbc_add_rig_quickrig['sna_wheels'])):
            bpy.context.view_layer.objects.active = rbc_add_rig_quickrig['sna_wheels'][i_C1E93]
            rbc_add_rig_quickrig['sna_wheels'][i_C1E93].select_set(state=True, )
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_C1E93].wheel_button = True
        bpy.ops.sna.generate_rig_6c502('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Quick_Rig_631Dc(bpy.types.Operator):
    bl_idname = "sna.quick_rig_631dc"
    bl_label = "Quick Rig"
    bl_description = "Generates and Sets up a rig with selected objects"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not (not (len(list(bpy.context.view_layer.objects.selected)) >= 3))

    def execute(self, context):
        bpy.context.scene.sna_rename_rig = False
        sna_find_dim_9A738()
        sna_assign_carwheels_E2BBF()
        sna_add_rbc_scene_DCE04()
        if (len(rbc_add_rig_quickrig['sna_wheels']) > 3):
            sna_quickrig_B3110(None, int(len(rbc_add_rig_quickrig['sna_wheels']) / 2.0), 2, None, None, None)
        else:
            if (2 == len(rbc_add_rig_quickrig['sna_wheels'])):
                sna_create_a_rig_C8491(None, 1, False, 1, 0, 0, 0, 0)
            else:
                if (len(rbc_add_rig_quickrig['sna_wheels']) == 3):
                    sna_create_a_rig_C8491(None, 1, False, 2, 0, 0, 0, 0)
        bpy.ops.sna.quick_rig_set__aa043('INVOKE_DEFAULT', )
        bpy.ops.sna.transfer_rbc_rig_props_to_collection_8e3a5('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


_6B7B0_running = False
class SNA_OT_Modal_Operator_6B7B0(bpy.types.Operator):
    bl_idname = "sna.modal_operator_6b7b0"
    bl_label = "Modal Operator"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    cursor = "CROSSHAIR"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        if not False or context.area.spaces[0].bl_rna.identifier == 'SpaceNodeEditor':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                pass
            except Exception as error:
                print(error)

    def execute(self, context):
        global _6B7B0_running
        _6B7B0_running = False
        context.window.cursor_set("DEFAULT")
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _6B7B0_running
        if not context.area or not _6B7B0_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.window.cursor_set('CROSSHAIR')
        try:
            pass
        except Exception as error:
            print(error)
        if event.type in ['RIGHTMOUSE', 'ESC']:
            self.execute(context)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        global _6B7B0_running
        if _6B7B0_running:
            _6B7B0_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            context.window_manager.modal_handler_add(self)
            _6B7B0_running = True
            return {'RUNNING_MODAL'}


@persistent
def frame_change_pre_handler_220F8(dummy):
    pass


@persistent
def frame_change_pre_handler_BD3FF(dummy):
    for i_F2E6B in range(len([])):
        pass


class SNA_OT_Rig_To_Cache_4Fb23(bpy.types.Operator):
    bl_idname = "sna.rig_to_cache_4fb23"
    bl_label = "Rig to Cache"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_E28ED in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
            sna_enabledisable_objs_animated_863FC(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_E28ED].wheel_rb, False)
            sna_enabledisable_objs_contraints_651EE(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_E28ED].wheel_rb, False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Rig_To_Animation_91E3F(bpy.types.Operator):
    bl_idname = "sna.rig_to_animation_91e3f"
    bl_label = "Rig to Animation"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
    sna_new_property: bpy.props.BoolProperty(name='New Property', description='', default=False)

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_0B24C in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
            sna_enabledisable_objs_contraints_651EE(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_0B24C].wheel_rb, True)
            sna_enabledisable_objs_animated_863FC(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_0B24C].wheel_rb, True)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Clear_Baked_Keys_94763(bpy.types.Operator):
    bl_idname = "sna.clear_baked_keys_94763"
    bl_label = "Clear Baked Keys"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        RigRBs = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][0].wheel_rb.name
        # Set the names of the objects to remove animation from
        object_names = RigRBs
        # Loop through the objects and remove their animation
        for obj_name in object_names:
            # Get the object
            obj = bpy.data.objects[obj_name]
            # Clear the object's animation data
            obj.animation_data_clear()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_enabledisable_objs_contraints_651EE(OBJ, Hide_Cons):
    for i_74F2E in range(len(OBJ.constraints)):
        if 'RBC' in OBJ.constraints[i_74F2E].name:
            OBJ.constraints[i_74F2E].enabled = Hide_Cons


def sna_enabledisable_objs_animated_863FC(OBJ, Make_Anim):
    OBJ.rigid_body.kinematic = Make_Anim
    OBJ.delta_rotation_euler = (0.0, (math.radians(0.0) if Make_Anim else math.radians(90.0)), 0.0)


class SNA_OT_Bake_To_Keys_3A4F6(bpy.types.Operator):
    bl_idname = "sna.bake_to_keys_3a4f6"
    bl_label = "Bake to Keys"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.sna.bake_ani_obj_action_e2073('INVOKE_DEFAULT', )
        bpy.ops.sna.rig_to_animation_91e3f('INVOKE_DEFAULT', sna_new_property=False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


@persistent
def frame_change_pre_handler_7EB4E(dummy):
    if False:
        for i_81BCF in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs)):
            obj = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_81BCF].obj
            obj.keyframe_insert(data_path="location")
            obj.keyframe_insert(data_path="rotation_euler")


@persistent
def frame_change_pre_handler_61194(dummy):
    pass


def sna_enable_constraint_EA6A7(Enable):
    for i_D98FE in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs)):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_D98FE].obj.rigid_body_constraint.enabled = Enable


def sna_add_to_ani_obj_collection_0CD06():
    item_503C6 = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs.add()
    item_503C6.name = bpy.context.view_layer.objects.active.name
    item_503C6.obj = bpy.context.view_layer.objects.active


def sna_add_rb_obj_list_8C6CF():
    rbc_animation_funcs['sna_rb_obj_list'] = []
    for i_13AB4 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        rbc_animation_funcs['sna_rb_obj_list'].append(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13AB4].body_rb)
    for i_A9A0B in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        rbc_animation_funcs['sna_rb_obj_list'].append(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_A9A0B].wheel_rb)


def sna_add_rb_anim_obj_B38AB(RB_Obj):
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
    bpy.ops.mesh.primitive_cube_add('INVOKE_DEFAULT', size=0.10000000149011612)
    bpy.context.view_layer.objects.active.name = RB_Obj.name + '.Ani'
    bpy.context.view_layer.objects.active.location = eval("bpy.data.objects['car.001'].matrix_world.translation".replace("'car.001'", "'" + RB_Obj.name + "'"))
    bpy.context.view_layer.objects.active.rotation_euler = eval("bpy.data.objects['car.001'].matrix_world.to_euler()".replace("'car.001'", "'" + RB_Obj.name + "'"))
    sna_add_to_ani_obj_collection_0CD06()
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, False, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection)
    bpy.ops.rigidbody.object_add('INVOKE_DEFAULT', type='ACTIVE')
    bpy.ops.rigidbody.constraint_add('INVOKE_DEFAULT', type='FIXED')
    bpy.context.view_layer.objects.active.rigid_body_constraint.object1 = bpy.context.view_layer.objects.active
    bpy.context.view_layer.objects.active.rigid_body_constraint.object2 = RB_Obj
    bpy.context.view_layer.objects.active.rigid_body.collision_collections = (False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False)
    bpy.context.view_layer.objects.active.rigid_body.mass = 0.10000000149011612


class SNA_OT_Add_Animation_Objs_5Ca5B(bpy.types.Operator):
    bl_idname = "sna.add_animation_objs_5ca5b"
    bl_label = "Add Animation Objs"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_E61E6 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
            sna_add_rb_anim_obj_B38AB(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_E61E6].body_rb)
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_E61E6].body_anim_obj = bpy.context.view_layer.objects.active
        for i_54491 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
            sna_add_rb_anim_obj_B38AB(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_54491].wheel_rb)
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_54491].wheel_animobj = bpy.context.view_layer.objects.active
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Delete_Animation_Objs_5E23A(bpy.types.Operator):
    bl_idname = "sna.delete_animation_objs_5e23a"
    bl_label = "Delete Animation Objs"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[0]", globals(), locals()):
            for i_99056 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs)):
                if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[0]", globals(), locals()):
                    bpy.data.meshes.remove(mesh=bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_99056].obj.data, )
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs.clear()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Bake_Ani_Obj_Action_E2073(bpy.types.Operator):
    bl_idname = "sna.bake_ani_obj_action_e2073"
    bl_label = "Bake Ani Obj Action"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
        for i_881CA in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs)):
            sna_hide_obj_select_71598(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_881CA].obj, False, True, False, False)
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_881CA].obj.select_set(state=True, )
        bpy.ops.nla.bake('INVOKE_DEFAULT', frame_start=bpy.context.scene.frame_start, frame_end=bpy.context.scene.frame_end, visual_keying=True, use_current_action=True, clean_curves=True, bake_types=set(['OBJECT']))
        sna_hide_obj_select_71598(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_881CA].obj, True, True, False, False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_set_anim_obj_to_rb_obj_5F210(Anim_Obj, RB_Obj):
    Anim_Obj.location = eval("bpy.data.objects['car.001'].matrix_world.translation".replace("'car.001'", "'" + RB_Obj.name + "'"))
    Anim_Obj.rotation_euler = eval("bpy.data.objects['car.001'].matrix_world.to_euler()".replace("'car.001'", "'" + RB_Obj.name + "'"))


def sna_disable_drivesteering_5F9C7(Input):
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].drivers.disable_drive = Input
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].drivers.disable_steering = Input


def sna_break_threshold_D598F(threshold):
    for i_CE865 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs)):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_CE865].obj.rigid_body_constraint.breaking_threshold = threshold


def sna_breakable_8997A(Enable):
    for i_86203 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs)):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_86203].obj.rigid_body_constraint.use_breaking = Enable


def sna_enable_kinematic_5DF45(Enable):
    for i_8F8D6 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs)):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_anim_objs[i_8F8D6].obj.rigid_body.kinematic = Enable


def sna_delete_anim_keys_54283():
    for i_FDD7C in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_FDD7C].body_anim_obj.animation_data_clear()
    for i_B637E in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_B637E].wheel_animobj.animation_data_clear()


@persistent
def frame_change_post_handler_0BC89(dummy):
    if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()):
        sna_breakable_8997A(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.enable_breakable)
        sna_break_threshold_D598F(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.breakable_threshold)


def sna_set_rb_kinemaitic_C8F94(Bol):
    sna_add_rb_obj_list_8C6CF()
    for i_3D3C5 in range(len(rbc_animation_funcs['sna_rb_obj_list'])):
        rbc_animation_funcs['sna_rb_obj_list'][i_3D3C5].rigid_body.kinematic = Bol


def sna_set_rig_to_baked_6939F(Input):
    if Input:
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.rig_keyframes_baked = True
    else:
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.rig_keyframes_baked = False


@persistent
def frame_change_post_handler_E5047(dummy):
    pass


@persistent
def frame_change_post_handler_BC81A(dummy):
    pass


def sna_delete_rb_keys_D5F91():
    for i_F933F in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_F933F].body_rb.animation_data_clear()
    for i_897C8 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_897C8].wheel_rb.animation_data_clear()


def sna_set_inverse_90D9F():
    for i_5ECDD in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        bpy.context.view_layer.objects.active = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_5ECDD].body_rb
        bpy.ops.constraint.childof_set_inverse('INVOKE_DEFAULT', constraint='RBC Child Of Rig Control', owner='OBJECT')
    for i_FC5F3 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        bpy.context.view_layer.objects.active = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_FC5F3].wheel_rb
        bpy.ops.constraint.childof_set_inverse('INVOKE_DEFAULT', constraint='RBC Child Of Rig Control', owner='OBJECT')


def sna_set_to_keyframe_47A7C(Input):
    for i_6A12C in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        if Input:
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_6A12C].body_rb.rigid_body.kinematic = True
        else:
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_6A12C].body_rb.rigid_body.kinematic = False
    for i_CF4DB in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        if Input:
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_CF4DB].wheel_rb.rigid_body.kinematic = True
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_CF4DB].wheel_rb.delta_rotation_euler = (0.0, 0.0, 0.0)
        else:
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_CF4DB].wheel_rb.rigid_body.kinematic = False
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_CF4DB].wheel_rb.delta_rotation_euler = (0.0, 1.5700000524520874, 0.0)


class SNA_OT_Delete_Keyframes_B761F(bpy.types.Operator):
    bl_idname = "sna.delete_keyframes_b761f"
    bl_label = "Delete Keyframes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        sna_delete_anim_keys_54283()
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.enable_anim_constraint = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Delete_Baked_Keyframes_03E9D(bpy.types.Operator):
    bl_idname = "sna.delete_baked_keyframes_03e9d"
    bl_label = "Delete Baked Keyframes"
    bl_description = "Deletes selected rigs baked keyframes"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        sna_delete_rb_keys_D5F91()
        sna_set_rb_kinemaitic_C8F94(False)
        sna_set_rig_to_baked_6939F(False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SNA_OT_Bake_Keyframes_7F7D6(bpy.types.Operator):
    bl_idname = "sna.bake_keyframes_7f7d6"
    bl_label = "Bake Keyframes"
    bl_description = "Bakes selected rigs action to keyframes (Cache needs to be Recorded)"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        sna_add_rb_obj_list_8C6CF()
        objects = rbc_animation_funcs['sna_rb_obj_list']
        # Get the current scene
        scene = bpy.context.scene
        # Set the current frame to the start of the timeline
        scene.frame_set(scene.frame_start)
        frame = bpy.context.scene.frame_current
        # Get a list of all objects in the scene
        # Iterate over all frames in the timeline
        while not bpy.context.scene.sna_is_recording:
            # Iterate over all objects in the list
            for obj in objects:
                # Set the object's location and rotation
                obj.location = obj.matrix_world.translation
                obj.rotation_euler = obj.matrix_world.to_euler()
                # Add keyframes for the object's location and rotation
                obj.keyframe_insert(data_path='location', index=-1)
                obj.keyframe_insert(data_path='rotation_euler', index=-1)
            # Set the current frame to the next frame
            scene.frame_set(scene.frame_current + 1)
        sna_euler_discontinuity_filter_36158()
        sna_set_to_keyframe_47A7C(True)
        sna_set_inverse_90D9F()
        sna_set_rig_to_baked_6939F(True)
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Operator_A72B9(bpy.types.Operator):
    bl_idname = "sna.operator_a72b9"
    bl_label = "Operator"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_euler_discontinuity_filter_36158():
    for i_A1A30 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        sna_hide_obj_select_71598(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_A1A30].body_rb, False, False, False, False)
        obj = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_A1A30].body_rb
        # Get the object you want to apply the Euler filter to
        blender_version = bpy.app.version
        use_temp_override = blender_version >= (3, 3, 0)
        # Select the object
        obj.select_set(True)
        # Get the object's animation data
        animation_data = obj.animation_data
        # Check if the object has animation data
        if animation_data:
            # Select all animation curves
            for fcurve in animation_data.action.fcurves:
                fcurve.select = True
            # Get the area where the Graph Editor is located
            graph_area = None
            for area in bpy.context.screen.areas:
                if area.type == 'GRAPH_EDITOR':
                    graph_area = area
                    break
            if graph_area:
                # Set the context to the Graph Editor
                ctx = bpy.context.copy()
                ctx['area'] = graph_area
                ctx['region'] = graph_area.regions[-1]
                if use_temp_override:
                    with bpy.context.temp_override(**ctx):
                        bpy.ops.graph.euler_filter()
                else:
                    bpy.ops.graph.euler_filter(ctx)
            else:
                # Store the current area type
                prev_area_type = bpy.context.area.type
                # Switch to the Graph Editor
                bpy.context.area.type = 'GRAPH_EDITOR'
                # Check if the Graph Editor is now active
                graph_area = None
                for area in bpy.context.screen.areas:
                    if area.type == 'GRAPH_EDITOR':
                        graph_area = area
                        break
                if graph_area:
                    # Set the context to the newly opened Graph Editor
                    ctx = bpy.context.copy()
                    ctx['area'] = graph_area
                    ctx['region'] = graph_area.regions[-1]
                    if use_temp_override:
                        with bpy.context.temp_override(**ctx):
                            bpy.ops.graph.euler_filter()
                    else:
                        bpy.ops.graph.euler_filter(ctx)
                else:
                    print("Graph Editor could not be opened.")
                bpy.context.area.type = prev_area_type
        else:
            print("No animation data found.")
        sna_hide_obj_select_71598(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_A1A30].body_rb, True, False, False, False)
    for i_BFC37 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        sna_hide_obj_select_71598(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_BFC37].wheel_rb, False, False, False, False)
        obj = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_BFC37].wheel_rb
        # Get the object you want to apply the Euler filter to
        blender_version = bpy.app.version
        use_temp_override = blender_version >= (3, 3, 0)
        # Select the object
        obj.select_set(True)
        # Get the object's animation data
        animation_data = obj.animation_data
        # Check if the object has animation data
        if animation_data:
            # Select all animation curves
            for fcurve in animation_data.action.fcurves:
                fcurve.select = True
            # Get the area where the Graph Editor is located
            graph_area = None
            for area in bpy.context.screen.areas:
                if area.type == 'GRAPH_EDITOR':
                    graph_area = area
                    break
            if graph_area:
                # Set the context to the Graph Editor
                ctx = bpy.context.copy()
                ctx['area'] = graph_area
                ctx['region'] = graph_area.regions[-1]
                if use_temp_override:
                    with bpy.context.temp_override(**ctx):
                        bpy.ops.graph.euler_filter()
                else:
                    bpy.ops.graph.euler_filter(ctx)
            else:
                # Store the current area type
                prev_area_type = bpy.context.area.type
                # Switch to the Graph Editor
                bpy.context.area.type = 'GRAPH_EDITOR'
                # Check if the Graph Editor is now active
                graph_area = None
                for area in bpy.context.screen.areas:
                    if area.type == 'GRAPH_EDITOR':
                        graph_area = area
                        break
                if graph_area:
                    # Set the context to the newly opened Graph Editor
                    ctx = bpy.context.copy()
                    ctx['area'] = graph_area
                    ctx['region'] = graph_area.regions[-1]
                    if use_temp_override:
                        with bpy.context.temp_override(**ctx):
                            bpy.ops.graph.euler_filter()
                    else:
                        bpy.ops.graph.euler_filter(ctx)
                else:
                    print("Graph Editor could not be opened.")
                bpy.context.area.type = prev_area_type
        else:
            print("No animation data found.")
        sna_hide_obj_select_71598(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_BFC37].wheel_rb, True, False, False, False)


@persistent
def frame_change_post_handler_30ABA(dummy):
    if bpy.context.scene.sna_animation_menu.record_keyframes:
        for i_C3FFE in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
            sna_set_anim_obj_to_rb_obj_5F210(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_C3FFE].body_anim_obj, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_C3FFE].body_rb)
            obj = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_C3FFE].body_anim_obj
            obj.keyframe_insert(data_path="location")
            obj.keyframe_insert(data_path="rotation_euler")
        for i_0CA55 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
            sna_set_anim_obj_to_rb_obj_5F210(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_0CA55].wheel_animobj, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_0CA55].wheel_rb)
            obj = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_0CA55].wheel_animobj
            obj.keyframe_insert(data_path="location")
            obj.keyframe_insert(data_path="rotation_euler")


class SNA_PT_NEW_PANEL_7C7C6(bpy.types.Panel):
    bl_label = 'New Panel'
    bl_idname = 'SNA_PT_NEW_PANEL_7C7C6'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'Animation'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (True)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.bake_ani_obj_action_e2073', text='Bake Keyframes', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.clear_baked_keys_94763', text='Clear Keyframes', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.add_animation_objs_5ca5b', text='Add Ani OBJs', icon_value=0, emboss=True, depress=False)
        op = layout.operator('sna.delete_animation_objs_5e23a', text='Delete Ani OBJs', icon_value=0, emboss=True, depress=False)


def sna_animation_rbc_collection_73E0B(layout_function, ):
    if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0):
        col_176B5 = layout_function.column(heading='', align=True)
        col_176B5.alert = False
        col_176B5.enabled = True
        col_176B5.active = True
        col_176B5.use_property_split = False
        col_176B5.use_property_decorate = False
        col_176B5.scale_x = 1.0
        col_176B5.scale_y = 1.0
        col_176B5.alignment = 'Expand'.upper()
        col_176B5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_A9892 = col_176B5.box()
        box_A9892.alert = False
        box_A9892.enabled = True
        box_A9892.active = True
        box_A9892.use_property_split = False
        box_A9892.use_property_decorate = False
        box_A9892.alignment = 'Expand'.upper()
        box_A9892.scale_x = 1.0
        box_A9892.scale_y = 1.0
        if not True: box_A9892.operator_context = "EXEC_DEFAULT"
        row_4C4D3 = box_A9892.row(heading='', align=True)
        row_4C4D3.alert = False
        row_4C4D3.enabled = True
        row_4C4D3.active = True
        row_4C4D3.use_property_split = False
        row_4C4D3.use_property_decorate = False
        row_4C4D3.scale_x = 1.2699999809265137
        row_4C4D3.scale_y = 1.100000023841858
        row_4C4D3.alignment = 'Expand'.upper()
        row_4C4D3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_4C4D3.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig], 'hide_rig', text='', icon_value=(253 if bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].hide_rig else 254), emboss=True)
        row_4C4D3.prop(bpy.context.scene, 'sna_auto_select_rig', text='', icon_value=(256 if bpy.context.scene.sna_auto_select_rig else 255), emboss=True, toggle=True)
        row_4C4D3.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig], 'rig_name', text='', icon_value=0, emboss=True)
        grid_C672B = box_A9892.grid_flow(columns=5, row_major=False, even_columns=True, even_rows=False, align=True)
        grid_C672B.enabled = True
        grid_C672B.active = True
        grid_C672B.use_property_split = False
        grid_C672B.use_property_decorate = False
        grid_C672B.alignment = 'Expand'.upper()
        grid_C672B.scale_x = 1.0
        grid_C672B.scale_y = 1.0
        if not True: grid_C672B.operator_context = "EXEC_DEFAULT"
        grid_C672B.prop(bpy.context.scene, 'sna_rbc_collection_list', text='', icon_value=37, emboss=True, expand=True, toggle=False)
        layout_function = box_A9892
        sna_keyframes_D474E(layout_function, )


class SNA_PT_RBC_ANIMATION_A2B91(bpy.types.Panel):
    bl_label = 'RBC Animation'
    bl_idname = 'SNA_PT_RBC_ANIMATION_A2B91'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 5
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not ((not property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals())))

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=81, scale=1.0)

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_animation_rbc_collection_73E0B(layout_function, )
        box_A317E = layout.box()
        box_A317E.alert = False
        box_A317E.enabled = True
        box_A317E.active = True
        box_A317E.use_property_split = False
        box_A317E.use_property_decorate = False
        box_A317E.alignment = 'Expand'.upper()
        box_A317E.scale_x = 1.0
        box_A317E.scale_y = 1.0
        if not True: box_A317E.operator_context = "EXEC_DEFAULT"
        layout_function = box_A317E
        sna_cache_panel_16EE9(layout_function, )


def sna_keyframes_D474E(layout_function, ):
    if bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.rig_keyframes_baked:
        col_57E33 = layout_function.column(heading='', align=False)
        col_57E33.alert = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_animation.rig_keyframes_baked
        col_57E33.enabled = True
        col_57E33.active = True
        col_57E33.use_property_split = False
        col_57E33.use_property_decorate = False
        col_57E33.scale_x = 1.0
        col_57E33.scale_y = 1.0
        col_57E33.alignment = 'Expand'.upper()
        col_57E33.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_57E33.operator('sna.delete_baked_keyframes_03e9d', text='Delete Keyframes', icon_value=0, emboss=True, depress=False)
    else:
        col_576D0 = layout_function.column(heading='', align=(bpy.context.scene.rigidbody_world.point_cache.info == rbc_animation_interface['sna_rbw_info']))
        col_576D0.alert = False
        col_576D0.enabled = bpy.context.scene.rigidbody_world.point_cache.is_baked
        col_576D0.active = True
        col_576D0.use_property_split = False
        col_576D0.use_property_decorate = False
        col_576D0.scale_x = 1.0
        col_576D0.scale_y = 1.0
        col_576D0.alignment = 'Expand'.upper()
        col_576D0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_576D0.operator('sna.bake_keyframes_7f7d6', text='Bake Keyframes', icon_value=0, emboss=True, depress=False)


def sna_play_button_6D9C5(layout_function, disable):
    split_27431 = layout_function.split(factor=0.699999988079071, align=True)
    split_27431.alert = False
    split_27431.enabled = disable
    split_27431.active = True
    split_27431.use_property_split = False
    split_27431.use_property_decorate = False
    split_27431.scale_x = 1.0
    split_27431.scale_y = 1.5
    split_27431.alignment = 'Expand'.upper()
    if not True: split_27431.operator_context = "EXEC_DEFAULT"
    if bpy.context.screen.is_animation_playing:
        op = split_27431.operator('screen.animation_play', text='Pause', icon_value=498, emboss=True, depress=False)
    else:
        op = split_27431.operator('screen.animation_play', text='Play', icon_value=495, emboss=True, depress=False)
    op = split_27431.operator('sna.playrest_simulation_0c324', text='Restart', icon_value=0, emboss=True, depress=False)


def sna_cache_panel_16EE9(layout_function, ):
    col_BDD20 = layout_function.column(heading='', align=False)
    col_BDD20.alert = False
    col_BDD20.enabled = True
    col_BDD20.active = True
    col_BDD20.use_property_split = False
    col_BDD20.use_property_decorate = False
    col_BDD20.scale_x = 1.0
    col_BDD20.scale_y = 1.0
    col_BDD20.alignment = 'Expand'.upper()
    col_BDD20.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_53039 = col_BDD20.column(heading='', align=False)
    col_53039.alert = bpy.context.scene.rigidbody_world.point_cache.is_baked
    col_53039.enabled = True
    col_53039.active = True
    col_53039.use_property_split = False
    col_53039.use_property_decorate = False
    col_53039.scale_x = 1.0
    col_53039.scale_y = 2.0
    col_53039.alignment = 'Expand'.upper()
    col_53039.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if bpy.context.scene.rigidbody_world.point_cache.is_baked:
        col_01C53 = col_53039.column(heading='', align=True)
        col_01C53.alert = True
        col_01C53.enabled = (not (bpy.context.scene.sna_is_recording and bpy.context.screen.is_animation_playing))
        col_01C53.active = True
        col_01C53.use_property_split = False
        col_01C53.use_property_decorate = False
        col_01C53.scale_x = 1.0
        col_01C53.scale_y = 1.0
        col_01C53.alignment = 'Expand'.upper()
        col_01C53.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_01C53.operator('sna.delete_current_cache_83f83', text=('Recording Cache' if (bpy.context.scene.sna_is_recording and bpy.context.screen.is_animation_playing) else 'Delete Cache'), icon_value=0, emboss=True, depress=False)
    else:
        col_304EA = col_53039.column(heading='', align=True)
        col_304EA.alert = False
        col_304EA.enabled = True
        col_304EA.active = True
        col_304EA.use_property_split = False
        col_304EA.use_property_decorate = False
        col_304EA.scale_x = 1.0
        col_304EA.scale_y = 1.0
        col_304EA.alignment = 'Expand'.upper()
        col_304EA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_3A3B8 = col_304EA.split(factor=0.699999988079071, align=True)
        split_3A3B8.alert = False
        split_3A3B8.enabled = True
        split_3A3B8.active = True
        split_3A3B8.use_property_split = False
        split_3A3B8.use_property_decorate = False
        split_3A3B8.scale_x = 1.0
        split_3A3B8.scale_y = 1.0
        split_3A3B8.alignment = 'Expand'.upper()
        if not True: split_3A3B8.operator_context = "EXEC_DEFAULT"
        op = split_3A3B8.operator('sna.record_simulation_22d2d', text='Record Cache', icon_value=626, emboss=True, depress=False)
        op = split_3A3B8.operator('sna.record__current_simulation_d1460', text='Current', icon_value=0, emboss=True, depress=False)
    layout_function = col_BDD20
    sna_play_button_6D9C5(layout_function, True)


_87D5C_running = False
class SNA_OT_Modal_Operator_87D5C(bpy.types.Operator):
    bl_idname = "sna.modal_operator_87d5c"
    bl_label = "Modal Operator"
    bl_description = "Auto-Records Keyframes to Drive /Steering/Brake Values"
    bl_options = {"REGISTER", "UNDO"}
    cursor = "CROSSHAIR"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        if not False or context.area.spaces[0].bl_rna.identifier == 'SpaceNodeEditor':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                pass
            except Exception as error:
                print(error)

    def execute(self, context):
        global _87D5C_running
        _87D5C_running = False
        context.window.cursor_set("DEFAULT")
        bpy.ops.screen.animation_cancel('INVOKE_DEFAULT', )
        # Check Blender version
        blender_version = bpy.app.version
        use_temp_override = blender_version >= (3, 3, 0)
        # Create an override dictionary with the desired scene and point cache
        override = {
            'scene': bpy.context.scene,
            'point_cache': bpy.context.scene.rigidbody_world.point_cache
        }
        override_temp = bpy.context.scene.rigidbody_world.point_cache
        if use_temp_override:
            # Use temp_override for Blender version >= 3.3.0
            with bpy.context.temp_override(point_cache = override_temp, ):
                # Free the bake for the specified override
                bpy.ops.ptcache.bake_from_cache('INVOKE_DEFAULT', )
        else:
            # Use the older method for Blender version < 3.3.0
            bpy.ops.ptcache.bake_from_cache(override)
        bpy.ops.sna.show_keyframes_0c226('INVOKE_DEFAULT', )
        bpy.ops.sna.keyframegroup_ae234('INVOKE_DEFAULT', )
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _87D5C_running
        if not context.area or not _87D5C_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.window.cursor_set('CROSSHAIR')
        try:
            keyframe_7AB3A = bpy.data.actions['RBC KeyFrame'].fcurves[1].keyframe_points.insert(frame=bpy.context.scene.frame_current, value=bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.steering, )
            keyframe_FD071 = bpy.data.actions['RBC KeyFrame'].fcurves[2].keyframe_points.insert(frame=bpy.context.scene.frame_current, value=bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.drive, )
            keyframe_6190F = bpy.data.actions['RBC KeyFrame'].fcurves[3].keyframe_points.insert(frame=bpy.context.scene.frame_current, value=(1.0 if bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.brake else 0.0), )
        except Exception as error:
            print(error)
        if event.type in ['RIGHTMOUSE', 'ESC']:
            self.execute(context)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        global _87D5C_running
        if _87D5C_running:
            _87D5C_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            None.rig_control_obj.select_set(state=True, )
            bpy.context.view_layer.objects.active = None.rig_control_obj
            bpy.ops.screen.animation_cancel('INVOKE_DEFAULT', )
            # Check Blender version
            blender_version = bpy.app.version
            use_temp_override = blender_version >= (3, 3, 0)
            # Create an override dictionary with the desired scene and point cache
            override = {
                'scene': bpy.context.scene,
                'point_cache': bpy.context.scene.rigidbody_world.point_cache
            }
            override_temp = bpy.context.scene.rigidbody_world.point_cache
            if use_temp_override:
                # Use temp_override for Blender version >= 3.3.0
                with bpy.context.temp_override(point_cache = override_temp, ):
                    # Free the bake for the specified override
                    bpy.ops.ptcache.free_bake('INVOKE_DEFAULT', )
            else:
                # Use the older method for Blender version < 3.3.0
                bpy.ops.ptcache.free_bake(override)
            bpy.context.scene.frame_set(2)
            bpy.context.scene.frame_set(1)
            bpy.ops.sna.insert_keyframes_6f941('INVOKE_DEFAULT', )
            bpy.ops.screen.animation_play('INVOKE_DEFAULT', )
            context.window_manager.modal_handler_add(self)
            _87D5C_running = True
            return {'RUNNING_MODAL'}


class SNA_OT_Insert_Keyframes_6F941(bpy.types.Operator):
    bl_idname = "sna.insert_keyframes_6f941"
    bl_label = "Insert Keyframes"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if property_exists("bpy.data.actions['RBC KeyFrame']", globals(), locals()):
            if (property_exists("bpy.data.actions['RBC KeyFrame'].fcurves[1]", globals(), locals()) and property_exists("bpy.data.actions['RBC KeyFrame'].fcurves[2]", globals(), locals()) and property_exists("bpy.data.actions['RBC KeyFrame'].fcurves[0]", globals(), locals())):
                pass
            else:
                fcurve_A7A7B = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='Empty', index=0, )
                fcurve_AE422 = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='sna_rig_control_drivers.steering', index=1, )
                fcurve_7ACD3 = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='.sna_rig_control_drivers.drive', index=2, )
                fcurve_DD2B7 = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='sna_rig_control_drivers.brake', index=3, )
                None.rig_control_obj.animation_data.action = bpy.data.actions['RBC KeyFrame']
        else:
            action_D95C2 = bpy.data.actions.new(name='RBC KeyFrame', )
            bpy.data.actions['RBC KeyFrame'].use_fake_user = True
            if (property_exists("bpy.data.actions['RBC KeyFrame'].fcurves[1]", globals(), locals()) and property_exists("bpy.data.actions['RBC KeyFrame'].fcurves[2]", globals(), locals()) and property_exists("bpy.data.actions['RBC KeyFrame'].fcurves[0]", globals(), locals())):
                pass
            else:
                fcurve_B4EAC = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='Empty', index=0, )
                fcurve_65074 = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='sna_rig_control_drivers.steering', index=1, )
                fcurve_CD9B5 = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='.sna_rig_control_drivers.drive', index=2, )
                fcurve_AF8B2 = bpy.data.actions['RBC KeyFrame'].fcurves.new(data_path='sna_rig_control_drivers.brake', index=3, )
                None.rig_control_obj.animation_data.action = bpy.data.actions['RBC KeyFrame']
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Keyframegroup_Ae234(bpy.types.Operator):
    bl_idname = "sna.keyframegroup_ae234"
    bl_label = "KeyFrameGroup"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        action_group_E9B38 = bpy.data.actions['RBC KeyFrame'].groups.new(name='KeyFrameGroup', )
        bpy.data.actions['RBC KeyFrame'].fcurves[1].group = bpy.data.actions['RBC KeyFrame'].groups['KeyFrameGroup']
        bpy.data.actions['RBC KeyFrame'].fcurves[2].group = bpy.data.actions['RBC KeyFrame'].groups['KeyFrameGroup']
        bpy.data.actions['RBC KeyFrame'].fcurves[3].group = bpy.data.actions['RBC KeyFrame'].groups['KeyFrameGroup']
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Disable_Keyframes_5Fc18(bpy.types.Operator):
    bl_idname = "sna.disable_keyframes_5fc18"
    bl_label = "Disable KeyFrames"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if bpy.data.actions['RBC KeyFrame'].fcurves[0].mute:
            bpy.data.actions['RBC KeyFrame'].fcurves[0].mute = False
            bpy.data.actions['RBC KeyFrame'].fcurves[1].mute = False
        else:
            bpy.data.actions['RBC KeyFrame'].fcurves[0].mute = True
            bpy.data.actions['RBC KeyFrame'].fcurves[1].mute = True
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Delete_Recorded_Keyframes_F1Cca(bpy.types.Operator):
    bl_idname = "sna.delete_recorded_keyframes_f1cca"
    bl_label = "Delete Recorded Keyframes?"
    bl_description = "Deletes Recorded Keyframe Values"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if property_exists("bpy.data.actions['RBC KeyFrame']", globals(), locals()):
            bpy.data.actions.remove(action=bpy.data.actions['RBC KeyFrame'], )
            # Check Blender version
            blender_version = bpy.app.version
            use_temp_override = blender_version >= (3, 3, 0)
            # Create an override dictionary with the desired scene and point cache
            override = {
                'scene': bpy.context.scene,
                'point_cache': bpy.context.scene.rigidbody_world.point_cache
            }
            override_temp = bpy.context.scene.rigidbody_world.point_cache
            if use_temp_override:
                # Use temp_override for Blender version >= 3.3.0
                with bpy.context.temp_override(point_cache = override_temp, ):
                    # Free the bake for the specified override
                    bpy.ops.ptcache.free_bake('INVOKE_DEFAULT', )
            else:
                # Use the older method for Blender version < 3.3.0
                bpy.ops.ptcache.free_bake(override)
            bpy.context.scene.frame_set(2)
            bpy.context.scene.frame_set(1)
            bpy.context.scene.frame_end = 2500
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SNA_OT_Show_Keyframes_0C226(bpy.types.Operator):
    bl_idname = "sna.show_keyframes_0c226"
    bl_label = "Show KeyFrames"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if property_exists("None", globals(), locals()):
            None.rig_control_obj.select_set(state=False, )
        else:
            bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
            None.rig_control_obj.select_set(state=True, )
            bpy.context.view_layer.objects.active = None.rig_control_obj
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


@persistent
def frame_change_post_handler_DD6BD(dummy):
    if ((bpy.context.scene.rigidbody_world.point_cache.info == bpy.context.scene.sna_rbw_info) and (bpy.context.scene.frame_current != bpy.context.scene.frame_end)):
        bpy.context.scene.sna_is_recording = False
    else:
        bpy.context.scene.sna_rbw_info = bpy.context.scene.rigidbody_world.point_cache.info
        bpy.context.scene.sna_is_recording = True


class SNA_OT_Delete_Current_Cache_83F83(bpy.types.Operator):
    bl_idname = "sna.delete_current_cache_83f83"
    bl_label = "Delete Current Cache?"
    bl_description = "Deletes Current Cache"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        # Check Blender version
        blender_version = bpy.app.version
        use_temp_override = blender_version >= (3, 3, 0)
        # Create an override dictionary with the desired scene and point cache
        override = {
            'scene': bpy.context.scene,
            'point_cache': bpy.context.scene.rigidbody_world.point_cache
        }
        override_temp = bpy.context.scene.rigidbody_world.point_cache
        if use_temp_override:
            # Use temp_override for Blender version >= 3.3.0
            with bpy.context.temp_override(point_cache = override_temp, ):
                # Free the bake for the specified override
                bpy.ops.ptcache.free_bake('INVOKE_DEFAULT', )
        else:
            # Use the older method for Blender version < 3.3.0
            bpy.ops.ptcache.free_bake(override)
        bpy.context.scene.frame_set(2)
        bpy.context.scene.frame_set(1)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SNA_OT_Playrest_Simulation_0C324(bpy.types.Operator):
    bl_idname = "sna.playrest_simulation_0c324"
    bl_label = "Play/Rest Simulation"
    bl_description = "Jumps to first frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Record__Current_Simulation_D1460(bpy.types.Operator):
    bl_idname = "sna.record__current_simulation_d1460"
    bl_label = "Record  Current Simulation"
    bl_description = "Records Cache to current frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        # Check Blender version
        blender_version = bpy.app.version
        use_temp_override = blender_version >= (3, 3, 0)
        # Create an override dictionary with the desired scene and point cache
        override = {
            'scene': bpy.context.scene,
            'point_cache': bpy.context.scene.rigidbody_world.point_cache
        }
        override_temp = bpy.context.scene.rigidbody_world.point_cache
        if use_temp_override:
            # Use temp_override for Blender version >= 3.3.0
            with bpy.context.temp_override(point_cache = override_temp, ):
                # Free the bake for the specified override
                bpy.ops.ptcache.bake_from_cache('INVOKE_DEFAULT', )
        else:
            # Use the older method for Blender version < 3.3.0
            bpy.ops.ptcache.bake_from_cache(override)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Record_Simulation_22D2D(bpy.types.Operator):
    bl_idname = "sna.record_simulation_22d2d"
    bl_label = "Record Simulation"
    bl_description = "Records Cache from start frame"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        # Check Blender version
        blender_version = bpy.app.version
        use_temp_override = blender_version >= (3, 3, 0)
        # Create an override dictionary with the desired scene and point cache
        override = {
            'scene': bpy.context.scene,
            'point_cache': bpy.context.scene.rigidbody_world.point_cache
        }
        override_temp = bpy.context.scene.rigidbody_world.point_cache
        if use_temp_override:
            # Use temp_override for Blender version >= 3.3.0
            with bpy.context.temp_override(point_cache = override_temp, ):
                # Free the bake for the specified override
                bpy.ops.ptcache.free_bake('INVOKE_DEFAULT', )
        else:
            # Use the older method for Blender version < 3.3.0
            bpy.ops.ptcache.free_bake(override)
        bpy.context.scene.frame_set(2)
        bpy.context.scene.frame_set(1)
        # Check Blender version
        blender_version = bpy.app.version
        use_temp_override = blender_version >= (3, 3, 0)
        # Create an override dictionary with the desired scene and point cache
        override = {
            'scene': bpy.context.scene,
            'point_cache': bpy.context.scene.rigidbody_world.point_cache
        }
        override_temp = bpy.context.scene.rigidbody_world.point_cache
        if use_temp_override:
            # Use temp_override for Blender version >= 3.3.0
            with bpy.context.temp_override(point_cache = override_temp, ):
                # Free the bake for the specified override
                bpy.ops.ptcache.bake_from_cache('INVOKE_DEFAULT', )
        else:
            # Use the older method for Blender version < 3.3.0
            bpy.ops.ptcache.bake_from_cache(override)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_rbc_rig_asset_list_enum_items(self, context):
    enum_items = [['Ambulance', 'Ambulance', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/Ambulance_Icon.jpg')], ['Bus', 'Bus', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/Bus_Icon.jpg')], ['Corvette', 'Corvette', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/Corvette_Icon.jpg')], ['Police Car', 'Police Car', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/Police_Car_Icon.jpg')], ['Sedan', 'Sedan', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/Sedan_Icon.jpg')], ['SUV', 'SUV', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/SUV_Icon.jpg')], ['Semi-Truck', 'Semi-Truck', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/Truck_Icon.jpg')], ['Wagon', 'Wagon', '', load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Asset RenderCrate Icons') + '/Wagon_Icon.jpg')]]
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


class SNA_OT_Transfer_Rbc_Rig_Props_To_Collection_8E3A5(bpy.types.Operator):
    bl_idname = "sna.transfer_rbc_rig_props_to_collection_8e3a5"
    bl_label = "Transfer RBC Rig Props to Collection"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.context.scene.sna_transfer_rig_props = True
        rbc_asset_library['sna_transer_rbc_rig_props_list'] = []
        output_0_f8a1d = sna_unregistered_rig_collections__CA180()
        rbc_asset_library['sna_transer_rbc_rig_props_list'] = output_0_f8a1d
        if (output_0_f8a1d != None):
            for i_3CCA4 in range(len(rbc_asset_library['sna_transer_rbc_rig_props_list'])):
                if (output_0_f8a1d != None):
                    rbc_asset_library['sna_transer_rbc_rig_props_list'][i_3CCA4].rig_collection.sna_rbc_asset_collection_properties.name = rbc_asset_library['sna_transer_rbc_rig_props_list'][i_3CCA4].name
                    sna_transfer_props_5BA0A(rbc_asset_library['sna_transer_rbc_rig_props_list'][i_3CCA4], rbc_asset_library['sna_transer_rbc_rig_props_list'][i_3CCA4].rig_collection.sna_rbc_asset_collection_properties, '')
        bpy.context.scene.sna_transfer_rig_props = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_check_if_overlapping_E7BD9():
    rbc_asset_library['sna_overlapping_rigs'] = []
    for i_5E9E8 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
        for i_E0D51 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            if (i_E0D51 != bpy.context.scene.sna_rbc_rig_collection.find(bpy.context.scene.sna_active_rig)):
                for i_F3C66 in range(len(bpy.context.scene.sna_rbc_rig_collection[i_E0D51].rig_bodies)):
                    is_overlap_0_d28ce, output_1_d28ce = sna_is_overlapping_1616C(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_5E9E8].body_rb, bpy.context.scene.sna_rbc_rig_collection[i_E0D51].rig_bodies[i_F3C66].body_rb, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj)
                    if (False if (is_overlap_0_d28ce == None) else is_overlap_0_d28ce):
                        rbc_asset_library['sna_overlapping_rigs'].append(bpy.context.scene.sna_rbc_rig_collection[i_E0D51].rig_control_obj)
    return [False, rbc_asset_library['sna_overlapping_rigs']]


def sna_is_overlapping_1616C(obj1, obj2, rig_control):
    obj1 = obj1
    obj2 = obj2
    rig_control = rig_control
    is_overlap = None
    overlap_dist = None
    from mathutils.bvhtree import BVHTree
    # Get the objects
    # Get their world matrix
    mat1 = obj1.matrix_world
    mat2 = obj2.matrix_world
    # Get the geometry in world coordinates
    vert1 = [mat1 @ v.co for v in obj1.data.vertices] 
    poly1 = [p.vertices for p in obj1.data.polygons]
    vert2 = [mat2 @ v.co for v in obj2.data.vertices] 
    poly2 = [p.vertices for p in obj2.data.polygons]
    # Create the BVH trees
    bvh1 = BVHTree.FromPolygons(vert1, poly1)
    bvh2 = BVHTree.FromPolygons(vert2, poly2)
    # Test for overlap
    overlap = bvh1.overlap(bvh2)
    if overlap:
        # The objects overlap
        is_overlap = True
        overlap_dist = bvh1.overlap(bvh2)[0][1]
    else:
        # The objects don't overlap
        is_overlap = False
    return [is_overlap, overlap_dist]


def sna_set_overlapping_location_3EF53(obj1, obj2):
    obj_a = obj1
    obj_b = obj2
    # Define the objects we want to check for overlap
    # Get the dimensions of object A
    dim_a = obj_a.dimensions.x
    # Get the location of object A
    loc_a = obj_a.location.x
    # Get the dimensions of object B
    dim_b = obj_b.dimensions.x
    # Get the location of object B
    loc_b = obj_b.location.x
    # Check if Object B is on the left or right side of Object A
    overlap_distance = (loc_b - dim_b/2) - (loc_a + dim_a/2)
    obj_a.location.x += overlap_distance


class SNA_OT_Rig_Overlap_Detection_B281A(bpy.types.Operator):
    bl_idname = "sna.rig_overlap_detection_b281a"
    bl_label = "Rig Overlap Detection"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if (len(sna_check_if_overlapping_E7BD9()[1]) > 0):
            for i_1AB88 in range(len(sna_check_if_overlapping_E7BD9()[1])):
                sna_set_overlapping_location_3EF53(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj, sna_check_if_overlapping_E7BD9()[1][i_1AB88])
        if (len(sna_check_if_overlapping_E7BD9()[1]) > 0):
            bpy.ops.sna.rig_overlap_detection_b281a('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Rig_Placement_84D02(bpy.types.Operator):
    bl_idname = "sna.rig_placement_84d02"
    bl_label = "Rig Placement"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if bpy.context.scene.sna_asset_placement == "Center":
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location = (0.0, 0.0, 0.0)
        elif bpy.context.scene.sna_asset_placement == "Cursor":
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location = bpy.context.scene.cursor.location
        else:
            pass
        bpy.ops.sna.snap_to_ground_f6c01('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_RBC_ASSETS_BE12E(bpy.types.Panel):
    bl_label = 'RBC Assets'
    bl_idname = 'SNA_PT_RBC_ASSETS_BE12E'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=124, scale=1.0)

    def draw(self, context):
        layout = self.layout
        col_98561 = layout.column(heading='', align=False)
        col_98561.alert = False
        col_98561.enabled = True
        col_98561.active = True
        col_98561.use_property_split = False
        col_98561.use_property_decorate = False
        col_98561.scale_x = 1.0
        col_98561.scale_y = 1.0
        col_98561.alignment = 'Expand'.upper()
        col_98561.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_98561.template_icon_view(bpy.context.scene, 'sna_rbc_rig_asset_list', show_labels=True, scale=5.0, scale_popup=5.0)
        op = col_98561.operator('sna.import_rbc_asset_rig_5beb8', text='Import Vehicle', icon_value=0, emboss=True, depress=False)
        row_90CBF = layout.row(heading='', align=False)
        row_90CBF.alert = False
        row_90CBF.enabled = True
        row_90CBF.active = True
        row_90CBF.use_property_split = False
        row_90CBF.use_property_decorate = False
        row_90CBF.scale_x = 1.0
        row_90CBF.scale_y = 1.0
        row_90CBF.alignment = 'Expand'.upper()
        row_90CBF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_90CBF.prop(bpy.context.scene, 'sna_asset_placement', text=' ', icon_value=0, emboss=True, expand=True)
        layout.label(text='Usage Rights: Editorial License', icon_value=110)
        layout.label(text='Vehicle Models Provided by ProductionCrate', icon_value=0)


def sna_set_roll_constraint_C9306():
    if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][0].physics_roll_constraint.rigid_body_constraint.object1 == None):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][0].physics_roll_constraint.rigid_body_constraint.object1 = bpy.context.scene.sna_rbc_scene_.ground


class SNA_OT_Import_Rbc_Asset_Rig_5Beb8(bpy.types.Operator):
    bl_idname = "sna.import_rbc_asset_rig_5beb8"
    bl_label = "Import RBC Asset Rig"
    bl_description = "Imports Selected RBC Asset"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_rbc_addon_collection == None):
            sna_add_rbc_scene_DCE04()
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'RBC RenderCrate Assets.blend') + r'\Collection', filename='RBC ' + bpy.context.scene.sna_rbc_rig_asset_list + ' Rig', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended_991CA = None if not new_data else new_data[0]
        bpy.context.scene.sna_transfer_rig_props = True
        sna_add_rig_to_rbc_rig_collection_A7613(appended_991CA)
        bpy.context.scene.sna_transfer_rig_props = False
        bpy.ops.sna.rig_placement_84d02('INVOKE_DEFAULT', )
        bpy.ops.sna.rig_overlap_detection_b281a('INVOKE_DEFAULT', )
        sna_set_roll_constraint_C9306()
        appended_991CA.sna_rbc_asset_collection = True
        bpy.context.scene.sna_rbc_rig_panel = set(['Controls'])
        bpy.ops.sna.reset_tire_friction_a0520('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_transfer_props_5BA0A(Scene_Prop, Asset_Coll_Prop, Name):
    Asset_Coll_Prop.rig_control_obj = Scene_Prop.rig_control_obj
    for i_A1E48 in range(len(Scene_Prop.rig_obj_collection)):
        item_4C6A1 = Asset_Coll_Prop.rig_obj_collection.add()
        item_4C6A1.name = Scene_Prop.rig_obj_collection[i_A1E48].obj.name
        item_4C6A1.obj = Scene_Prop.rig_obj_collection[i_A1E48].obj
    for i_78799 in range(len(Scene_Prop.rig_model_collection)):
        item_16C2C = Asset_Coll_Prop.rig_model_collection.add()
        item_16C2C.name = Scene_Prop.rig_model_collection[i_78799].obj.name
        item_16C2C.obj = Scene_Prop.rig_model_collection[i_78799].obj
    Asset_Coll_Prop.rig_collection = Scene_Prop.rig_collection
    Asset_Coll_Prop.rig_rigged = Scene_Prop.rig_rigged
    Asset_Coll_Prop.rig_type = Scene_Prop.rig_type
    for i_FC7D1 in range(len(Scene_Prop.rig_bodies)):
        item_C8048 = Asset_Coll_Prop.rig_bodies.add()
        item_C8048.name = Scene_Prop.rig_bodies[i_FC7D1].name
        item_C8048.body_button = True
        item_C8048.body_rb = Scene_Prop.rig_bodies[i_FC7D1].body_rb
        item_C8048.body_model = Scene_Prop.rig_bodies[i_FC7D1].body_model
        item_C8048.body_hitch_obj = Scene_Prop.rig_bodies[i_FC7D1].body_hitch_obj
        item_C8048.body_tuning_button = Scene_Prop.rig_bodies[i_FC7D1].body_tuning_button
        item_C8048.physics_weight = Scene_Prop.rig_bodies[i_FC7D1].physics_weight
        item_C8048.physics_weight_position_button = Scene_Prop.rig_bodies[i_FC7D1].physics_weight_position_button
        item_C8048.physics_roll_constraint = Scene_Prop.rig_bodies[i_FC7D1].physics_roll_constraint
        item_C8048.physics_roll_constraint_button = Scene_Prop.rig_bodies[i_FC7D1].physics_roll_constraint_button
        item_C8048.body_boundingbox = Scene_Prop.rig_bodies[i_FC7D1].body_boundingbox
        item_C8048.body_anim_obj = Scene_Prop.rig_bodies[i_FC7D1].body_anim_obj
    Asset_Coll_Prop.rig_name = Scene_Prop.rig_name
    Asset_Coll_Prop.rig_drivers.steering = Scene_Prop.rig_drivers.steering
    Asset_Coll_Prop.rig_drivers.torque = Scene_Prop.rig_drivers.torque
    Asset_Coll_Prop.rig_drivers.brake = Scene_Prop.rig_drivers.brake
    Asset_Coll_Prop.rig_drivers.brake_strength = Scene_Prop.rig_drivers.brake_strength
    Asset_Coll_Prop.rig_drivers.drive = Scene_Prop.rig_drivers.drive
    Asset_Coll_Prop.rig_drivers.disable_drive = Scene_Prop.rig_drivers.disable_drive
    Asset_Coll_Prop.rig_drivers.disable_steering = Scene_Prop.rig_drivers.disable_steering


class SNA_PT_RBC_COLLISIONS_3D783(bpy.types.Panel):
    bl_label = 'RBC Collisions'
    bl_idname = 'SNA_PT_RBC_COLLISIONS_3D783'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 6
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not ((not (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0)))

    def draw_header(self, context):
        layout = self.layout
        layout.label(text='', icon_value=282)

    def draw(self, context):
        layout = self.layout
        layout.label(text='Collision Type', icon_value=0)
        grid_D7073 = layout.grid_flow(columns=1, row_major=False, even_columns=False, even_rows=False, align=True)
        grid_D7073.enabled = True
        grid_D7073.active = True
        grid_D7073.use_property_split = False
        grid_D7073.use_property_decorate = False
        grid_D7073.alignment = 'Expand'.upper()
        grid_D7073.scale_x = 1.0
        grid_D7073.scale_y = 1.0
        if not True: grid_D7073.operator_context = "EXEC_DEFAULT"
        row_39EAA = grid_D7073.row(heading='', align=True)
        row_39EAA.alert = False
        row_39EAA.enabled = True
        row_39EAA.active = True
        row_39EAA.use_property_split = False
        row_39EAA.use_property_decorate = False
        row_39EAA.scale_x = 1.0
        row_39EAA.scale_y = 1.0
        row_39EAA.alignment = 'Expand'.upper()
        row_39EAA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_39EAA.operator('sna.make_collision_active_op_38f01', text='Active Collision', icon_value=0, emboss=True, depress=(sna_get_rb_type_E3B22() == 'ACTIVE'))
        op = row_39EAA.operator('sna.make_collision_passive_op_8c0c0', text='Passive Collision', icon_value=0, emboss=True, depress=(sna_get_rb_type_E3B22() == 'PASSIVE'))
        op = grid_D7073.operator('sna.clear_collision_ops_1f7f2', text='Clear Collision', icon_value=0, emboss=True, depress=False)
        op = layout.operator('rigidbody.object_settings_copy', text='Copy From Active', icon_value=0, emboss=True, depress=False)


class SNA_OT_Clear_Collision_Ops_1F7F2(bpy.types.Operator):
    bl_idname = "sna.clear_collision_ops_1f7f2"
    bl_label = "Clear Collision OPS"
    bl_description = "Clears Object's Rigid Body"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_7B91D in range(len(bpy.context.view_layer.objects.selected)):
            sna_clear_collision_function_func_0325D(bpy.context.view_layer.objects.selected[i_7B91D])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Make_Collision_Passive_Op_8C0C0(bpy.types.Operator):
    bl_idname = "sna.make_collision_passive_op_8c0c0"
    bl_label = "Make Collision Passive OP"
    bl_description = "Makes Selected Object a Passive Rigid Body"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_AC646 in range(len(bpy.context.view_layer.objects.selected)):
            sna_make_collision_passive_fun_C42BB(bpy.context.view_layer.objects.selected[i_AC646])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Make_Collision_Active_Op_38F01(bpy.types.Operator):
    bl_idname = "sna.make_collision_active_op_38f01"
    bl_label = "Make Collision Active OP"
    bl_description = "Makes Selected Object an Active Rigid Body"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_9ACB9 in range(len(bpy.context.view_layer.objects.selected)):
            sna_make_collision_active_func_0E4F7(bpy.context.view_layer.objects.selected[i_9ACB9])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_add_to_physics_pt_rigid_body_collisions_027B3(self, context):
    if not ((not (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0))):
        layout = self.layout
        split_35C9A = layout.split(factor=0.37437647581100464, align=False)
        split_35C9A.alert = False
        split_35C9A.enabled = True
        split_35C9A.active = True
        split_35C9A.use_property_split = False
        split_35C9A.use_property_decorate = False
        split_35C9A.scale_x = 1.0
        split_35C9A.scale_y = 1.0
        split_35C9A.alignment = 'Expand'.upper()
        if not True: split_35C9A.operator_context = "EXEC_DEFAULT"
        split_35C9A.label(text='', icon_value=0)
        split_277FE = split_35C9A.split(factor=0.75, align=False)
        split_277FE.alert = False
        split_277FE.enabled = True
        split_277FE.active = True
        split_277FE.use_property_split = False
        split_277FE.use_property_decorate = False
        split_277FE.scale_x = 1.0
        split_277FE.scale_y = 1.0
        split_277FE.alignment = 'Expand'.upper()
        if not True: split_277FE.operator_context = "EXEC_DEFAULT"
        op = split_277FE.operator('sna.show_convex_hull_aab03', text='Convex Hull', icon_value=(254 if property_exists("bpy.context.view_layer.objects.active.modifiers['RBC Convex Hull Nodes']", globals(), locals()) else 253), emboss=True, depress=property_exists("bpy.context.view_layer.objects.active.modifiers['RBC Convex Hull Nodes']", globals(), locals()))
        if property_exists("bpy.context.view_layer.objects.active.modifiers['RBC Convex Hull Nodes']", globals(), locals()):
            pass


def sna_append_convex_hull_node_30223():
    if property_exists("bpy.data.node_groups['RBC Convex Hull Nodes']", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'RBC Assets.blend') + r'\NodeTree', filename='RBC Convex Hull Nodes', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_EEC85 = None if not new_data else new_data[0]


def sna_make_collision_active_func_0E4F7(Input):
    sna_obj_prep_BC366()
    bpy.ops.rigidbody.objects_add('INVOKE_DEFAULT', type='ACTIVE')
    Input.rigid_body.collision_collections = (True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)


def sna_clear_collision_function_func_0325D(OBJ):
    if OBJ.rigid_body:
        bpy.context.view_layer.objects.active = OBJ
        bpy.ops.rigidbody.object_remove('INVOKE_DEFAULT', )


def sna_make_collision_passive_fun_C42BB(Input):
    sna_obj_prep_BC366()
    bpy.ops.rigidbody.objects_add('INVOKE_DEFAULT', type='PASSIVE')
    Input.rigid_body.collision_collections = (True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)


def sna_get_rb_type_E3B22():
    if (bpy.context.view_layer.objects.active != None):
        if bpy.context.view_layer.objects.active.rigid_body:
            return bpy.context.view_layer.objects.active.rigid_body.type


class SNA_OT_Show_Convex_Hull_Aab03(bpy.types.Operator):
    bl_idname = "sna.show_convex_hull_aab03"
    bl_label = "Show Convex Hull"
    bl_description = "Shows Convex Hull Collision Boundries using GeometryNodes"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        sna_append_convex_hull_node_30223()
        for i_197D0 in range(len(bpy.context.view_layer.objects.selected)):
            if property_exists("bpy.context.view_layer.objects.selected[i_197D0].modifiers['RBC Convex Hull Nodes']", globals(), locals()):
                bpy.context.view_layer.objects.selected[i_197D0].modifiers.remove(modifier=bpy.context.view_layer.objects.selected[i_197D0].modifiers['RBC Convex Hull Nodes'], )
            else:
                modifier_26794 = bpy.context.view_layer.objects.selected[i_197D0].modifiers.new(name='RBC Convex Hull Nodes', type='NODES', )
                modifier_26794.node_group = bpy.data.node_groups['RBC Convex Hull Nodes']
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_RIGID_BODY_WORLD_9E69D(bpy.types.Panel):
    bl_label = 'Rigid Body World'
    bl_idname = 'SNA_PT_RIGID_BODY_WORLD_9E69D'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 1
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (True)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout


def sna_custom_icon_93165(Rig_Type):
    return (load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_QuickRig_Icon.png')) if (Rig_Type == 'Quick Rig') else (load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Semi-Truck_icon.png')) if (Rig_Type == 'Semi-Truck') else (load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Truck_icon.png')) if (Rig_Type == 'Truck') else (37 if (Rig_Type == 'Car') else (load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Motorcycle_icon.png')) if (Rig_Type == 'Motorcycle') else 37)))))


def sna_rbc_collection_list_enum_items(self, context):
    enum_items = sna_rbc_list_7C4A6()
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_rbc_list_7C4A6():
    rigging_parts['sna_rbc_list'] = []
    for i_E0694 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
        rigging_parts['sna_rbc_list'].append([bpy.context.scene.sna_rbc_rig_collection[i_E0694].name, bpy.context.scene.sna_rbc_rig_collection[i_E0694].name, bpy.context.scene.sna_rbc_rig_collection[i_E0694].rig_name, sna_custom_icon_93165(bpy.context.scene.sna_rbc_rig_collection[i_E0694].rig_type)])
    return rigging_parts['sna_rbc_list']


def sna_rename_duplicate_names_DDA57(Name):
    rbc_rig_collection['sna_name'] = ''
    rbc_rig_collection['sna_name'] = Name
    if ((property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and rbc_rig_collection['sna_name'] in bpy.context.scene.sna_rbc_rig_collection) and (bpy.context.scene.sna_rbc_rig_collection.find(rbc_rig_collection['sna_name']) != bpy.context.scene.sna_rbc_rig_collection.find(bpy.context.scene.sna_active_rig))):
        bpy.context.scene.sna_rbc_rig_collection[rbc_rig_collection['sna_name']].rig_name = rbc_rig_collection['sna_name'] + '.00' + str(bpy.context.scene.sna_rbc_rig_collection.find(rbc_rig_collection['sna_name']))
        bpy.context.scene.sna_rbc_rig_collection[rbc_rig_collection['sna_name']].rig_collection.sna_rbc_asset_collection_properties.name = rbc_rig_collection['sna_name']


def sna_unregistered_rig_collections__CA180():
    rbc_rig_collection['sna_unregistered_rig_collection_list'] = []
    if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0):
        for i_B2C34 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            if bpy.context.scene.sna_rbc_rig_collection[i_B2C34].rig_rigged:
                if (len(bpy.context.scene.sna_rbc_rig_collection[i_B2C34].rig_collection.sna_rbc_asset_collection_properties.name) > 0):
                    pass
                else:
                    rbc_rig_collection['sna_unregistered_rig_collection_list'].append(bpy.context.scene.sna_rbc_rig_collection[i_B2C34])
        return rbc_rig_collection['sna_unregistered_rig_collection_list']


def sna_check_for_collection_assets_C84E7():
    rbc_rig_collection['sna_unregistered_rig_collection_asset_list'] = []
    for i_FCE31 in range(len(bpy.data.collections)):
        if (len(bpy.data.collections[i_FCE31].sna_rbc_asset_collection_properties.name) > 0):
            if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0):
                if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and bpy.data.collections[i_FCE31].sna_rbc_asset_collection_properties.name in bpy.context.scene.sna_rbc_rig_collection):
                    pass
                else:
                    rbc_rig_collection['sna_unregistered_rig_collection_asset_list'].append(bpy.data.collections[i_FCE31])
            else:
                rbc_rig_collection['sna_unregistered_rig_collection_asset_list'].append(bpy.data.collections[i_FCE31])
    return rbc_rig_collection['sna_unregistered_rig_collection_asset_list']


def sna_add_rig_to_rbc_rig_collection_A7613(Collection):
    item_AC091 = bpy.context.scene.sna_rbc_rig_collection.add()
    item_AC091.name = item_AC091.name + '.00' + str(bpy.context.scene.sna_rbc_rig_collection.find(Collection.sna_rbc_asset_collection_properties.name))
    bpy.context.scene.sna_active_rig = item_AC091.name
    sna_transfer_props_5BA0A(Collection.sna_rbc_asset_collection_properties, item_AC091, item_AC091.name)
    bpy.context.scene.sna_rename_rig = True
    item_AC091.rig_name = Collection.sna_rbc_asset_collection_properties.name
    bpy.context.scene.sna_rbc_collection_list = item_AC091.name
    sna_link_collection_to_rbc_addon_collection_4AC89(Collection)
    sna_hide_active_rig_constraints_F46AB()


class SNA_OT_Refresh_Rbc_Collection2_Abaaf(bpy.types.Operator):
    bl_idname = "sna.refresh_rbc_collection2_abaaf"
    bl_label = "Refresh RBC Collection2"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_7DE7B in range(len(bpy.data.collections)):
            if (len(bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties.name) > 0):
                if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0):
                    for i_0A315 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
                        if (bpy.context.scene.sna_rbc_rig_collection[i_0A315].name == bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties.name):
                            pass
                        else:
                            item_CF5F8 = bpy.context.scene.sna_rbc_rig_collection.add()
                            item_CF5F8.name = bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties.name + str(i_7DE7B)
                            bpy.context.scene.sna_active_rig = item_CF5F8.name
                            sna_transfer_props_5BA0A(bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties, item_CF5F8, bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties.name)
                            bpy.context.view_layer.layer_collection.collection.children['RBC Addon'].children.link(child=item_CF5F8.rig_collection, )
                else:
                    item_39BFC = bpy.context.scene.sna_rbc_rig_collection.add()
                    item_39BFC.name = bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties.name + '' + str(i_7DE7B)
                    bpy.context.scene.sna_active_rig = item_39BFC.name
                    sna_transfer_props_5BA0A(bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties, item_39BFC, bpy.data.collections[i_7DE7B].sna_rbc_asset_collection_properties.name)
                    bpy.context.view_layer.layer_collection.collection.children['RBC Addon'].children.link(child=item_39BFC.rig_collection, )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_check_for_collection_assets_in_scene_52BE9():
    for i_51A40 in range(len(bpy.data.collections)):
        if (len(bpy.data.collections[i_51A40].sna_rbc_asset_collection_properties.name) > 0):
            return bpy.data.collections[i_51A40].sna_rbc_asset_collection_properties.name


def sna_delete_obj_data_A5751(obj):
    if (obj != None):
        for i_5D67F in range(len(obj.material_slots)):
            if (obj.material_slots[i_5D67F].material != None):
                for i_C4120 in range(len(obj.material_slots[i_5D67F].material.node_tree.nodes)):
                    if (obj.material_slots[i_5D67F].material.node_tree.nodes[i_C4120].type == 'TEX_IMAGE'):
                        if (obj.material_slots[i_5D67F].material.node_tree.nodes[i_C4120].image != None):
                            bpy.data.images.remove(image=obj.material_slots[i_5D67F].material.node_tree.nodes[i_C4120].image, )
            if (obj.material_slots[i_5D67F].material != None):
                bpy.data.materials.remove(material=obj.material_slots[i_5D67F].material, )
        if (obj.data != None):
            bpy.data.meshes.remove(mesh=obj.data, )


class SNA_OT_Delete_Rbc_Rig__0De67(bpy.types.Operator):
    bl_idname = "sna.delete_rbc_rig__0de67"
    bl_label = "Delete RBC Rig "
    bl_description = "Deletes RBC Rig"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        bpy.ops.sna.clear_model_constraints_43579('INVOKE_DEFAULT', )
        bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
        rigging_parts['sna_delete_list'] = []
        for i_4B82E in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection)):
            rigging_parts['sna_delete_list'].append(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_4B82E].obj)
        if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection.sna_rbc_asset_collection if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection.sna_rbc_asset_collection", globals(), locals()) else False):
            for i_D25D6 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection)):
                if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection[i_D25D6].obj != None):
                    rigging_parts['sna_delete_list'].append(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection[i_D25D6].obj)
        for i_9BE8A in range(len(rigging_parts['sna_delete_list'])):
            if (rigging_parts['sna_delete_list'][i_9BE8A] != None):
                if rigging_parts['sna_delete_list'][i_9BE8A].type == 'MESH':
                    sna_delete_obj_data_A5751(rigging_parts['sna_delete_list'][i_9BE8A])
                else:
                    if property_exists("rigging_parts['sna_delete_list'][i_9BE8A].constraints['Child Of RB Wheel']", globals(), locals()):
                        rigging_parts['sna_delete_list'][i_9BE8A].constraints.remove(constraint=rigging_parts['sna_delete_list'][i_9BE8A].constraints['Child Of RB Wheel'], )
                    bpy.data.objects.remove(object=rigging_parts['sna_delete_list'][i_9BE8A], )
        if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection != None):
            bpy.data.collections.remove(collection=bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection, )
        if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()):
            for i_26C09 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
                if bpy.context.scene.sna_rbc_rig_collection[i_26C09] == bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]:
                    bpy.context.scene.sna_rbc_rig_collection.remove(i_26C09)
                    break
            if property_exists("bpy.context.scene.sna_rbc_rig_collection[-1]", globals(), locals()):
                bpy.context.scene.sna_rbc_collection_list = bpy.context.scene.sna_rbc_rig_collection[-1].name
                bpy.context.scene.sna_active_rig = bpy.context.scene.sna_rbc_rig_collection[-1].name
            else:
                bpy.context.scene.sna_active_rig = ''
            bpy.context.view_layer.objects.active = list(bpy.context.view_layer.objects)[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


@persistent
def load_pre_handler_1F36E(dummy):
    bpy.context.scene.sna_rbc_rig_collection.clear()


class SNA_OT_Refresh_Rbc_Collection_Bf32F(bpy.types.Operator):
    bl_idname = "sna.refresh_rbc_collection_bf32f"
    bl_label = "Refresh RBC Collection"
    bl_description = "Refreshes RBC Collection to add appended rigs"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_rbc_addon_collection == None):
            sna_add_rbc_scene_DCE04()
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
        rbc_rig_collection['sna_refresh_asset_collection_list'] = []
        if (sna_check_for_collection_assets_C84E7() != None):
            rbc_rig_collection['sna_refresh_asset_collection_list'] = sna_check_for_collection_assets_C84E7()
            for i_D6814 in range(len(rbc_rig_collection['sna_refresh_asset_collection_list'])):
                item_D289D = bpy.context.scene.sna_rbc_rig_collection.add()
                if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and rbc_rig_collection['sna_refresh_asset_collection_list'][i_D6814].sna_rbc_asset_collection_properties.name in bpy.context.scene.sna_rbc_rig_collection):
                    item_D289D.name = rbc_rig_collection['sna_refresh_asset_collection_list'][i_D6814].sna_rbc_asset_collection_properties.name + '.00' + str(bpy.context.scene.sna_rbc_rig_collection.find(rbc_rig_collection['sna_refresh_asset_collection_list'][i_D6814].sna_rbc_asset_collection_properties.name))
                else:
                    item_D289D.name = rbc_rig_collection['sna_refresh_asset_collection_list'][i_D6814].sna_rbc_asset_collection_properties.name
                bpy.context.scene.sna_active_rig = item_D289D.name
                sna_transfer_props_5BA0A(rbc_rig_collection['sna_refresh_asset_collection_list'][i_D6814].sna_rbc_asset_collection_properties, item_D289D, rbc_rig_collection['sna_refresh_asset_collection_list'][i_D6814].sna_rbc_asset_collection_properties.name)
                if item_D289D.rig_collection in list(bpy.data.collections['RBC Addon'].children):
                    pass
                else:
                    bpy.data.collections['RBC Addon'].children.link(child=item_D289D.rig_collection, )
                bpy.ops.sna.rig_overlap_detection_b281a('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_rbc_collection_F21DC(layout_function, ):
    if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0):
        col_56073 = layout_function.column(heading='', align=True)
        col_56073.alert = False
        col_56073.enabled = True
        col_56073.active = True
        col_56073.use_property_split = False
        col_56073.use_property_decorate = False
        col_56073.scale_x = 1.0
        col_56073.scale_y = 1.0
        col_56073.alignment = 'Expand'.upper()
        col_56073.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_56073.operator('sna.delete_rbc_rig__0de67', text='Delete Rig', icon_value=33, emboss=True, depress=False)
        box_00C74 = col_56073.box()
        box_00C74.alert = False
        box_00C74.enabled = True
        box_00C74.active = True
        box_00C74.use_property_split = False
        box_00C74.use_property_decorate = False
        box_00C74.alignment = 'Expand'.upper()
        box_00C74.scale_x = 1.0
        box_00C74.scale_y = 1.0
        if not True: box_00C74.operator_context = "EXEC_DEFAULT"
        row_08CF0 = box_00C74.row(heading='', align=True)
        row_08CF0.alert = False
        row_08CF0.enabled = True
        row_08CF0.active = True
        row_08CF0.use_property_split = False
        row_08CF0.use_property_decorate = False
        row_08CF0.scale_x = 1.0
        row_08CF0.scale_y = 1.100000023841858
        row_08CF0.alignment = 'Expand'.upper()
        row_08CF0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_08CF0.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig], 'hide_rig', text='', icon_value=(253 if bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].hide_rig else 254), emboss=True)
        row_08CF0.prop(bpy.context.scene, 'sna_auto_select_rig', text='', icon_value=(256 if bpy.context.scene.sna_auto_select_rig else 255), emboss=True, toggle=True)
        row_08CF0.prop(bpy.context.scene, 'sna_rename_rig', text='', icon_value=742, emboss=True, toggle=True)
        row_08CF0.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig], 'rig_name', text='', icon_value=0, emboss=True)
        grid_424F1 = box_00C74.grid_flow(columns=5, row_major=False, even_columns=True, even_rows=False, align=True)
        grid_424F1.enabled = True
        grid_424F1.active = True
        grid_424F1.use_property_split = False
        grid_424F1.use_property_decorate = False
        grid_424F1.alignment = 'Expand'.upper()
        grid_424F1.scale_x = 1.0
        grid_424F1.scale_y = 1.0
        if not True: grid_424F1.operator_context = "EXEC_DEFAULT"
        grid_424F1.prop(bpy.context.scene, 'sna_rbc_collection_list', text='', icon_value=37, emboss=True, expand=True, toggle=False)


def sna_check_for_collection_assets_button_06AD6():
    if (sna_check_for_collection_assets_C84E7() != None):
        return (len(sna_check_for_collection_assets_C84E7()) > 0)


def sna_unregistered_rig_collections_button_EDF15():
    if (sna_unregistered_rig_collections__CA180() != None):
        return (len(sna_unregistered_rig_collections__CA180()) > 0)


class SNA_PT_RBC_COLLECTION_8ECBE(bpy.types.Panel):
    bl_label = 'RBC Collection'
    bl_idname = 'SNA_PT_RBC_COLLECTION_8ECBE'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 1
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (((not (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0)) and (sna_check_for_collection_assets_in_scene_52BE9() == None)))

    def draw_header(self, context):
        layout = self.layout
        if sna_check_for_collection_assets_button_06AD6():
            op = layout.operator('sna.refresh_rbc_collection_bf32f', text='', icon_value=692, emboss=True, depress=False)
        else:
            layout.template_icon(icon_value=22, scale=1.0)

    def draw(self, context):
        layout = self.layout
        layout_function = layout
        sna_rbc_collection_F21DC(layout_function, )
        if sna_unregistered_rig_collections_button_EDF15():
            op = layout.operator('sna.transfer_rbc_rig_props_to_collection_8e3a5', text='Update RBC Rigs', icon_value=692, emboss=True, depress=False)


def sna_disable_ray_visablilty_B5A59(obj, Input):
    obj.visible_camera = Input
    obj.visible_diffuse = Input
    obj.visible_glossy = Input
    obj.visible_transmission = Input
    obj.visible_volume_scatter = Input
    obj.visible_shadow = Input


class SNA_OT_Import_Xinput_A1516(bpy.types.Operator):
    bl_idname = "sna.import_xinput_a1516"
    bl_label = "Import XInput"
    bl_description = "Installs XInput: Install in Administrator Mode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        #https://b3d.interplanety.org/en/installing-python-packages-with-pip-in-blender-on-windows-10/
        import sys
        python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')
        target = os.path.join(sys.prefix, 'lib', 'site-packages')
        subprocess.call([python_exe, '-m', 'ensurepip'])
        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'pip'])
        subprocess.call([python_exe, '-m', 'pip', 'install', '--upgrade', 'XInput-Python', '-t', target])
        print('FINISHED')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


_FE555_running = False
class SNA_OT_Controller_Operator_Fe555(bpy.types.Operator):
    bl_idname = "sna.controller_operator_fe555"
    bl_label = "Controller Operator"
    bl_description = "Starts Controller Modal Operator"
    bl_options = {"REGISTER", "UNDO"}
    cursor = "DEFAULT"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        if not False or context.area.spaces[0].bl_rna.identifier == 'SpaceNodeEditor':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                pass
            except Exception as error:
                print(error)

    def execute(self, context):
        global _FE555_running
        _FE555_running = False
        context.window.cursor_set("DEFAULT")
        bpy.ops.screen.animation_play('INVOKE_DEFAULT', )
        bpy.ops.sna.drive_reset_d354c('INVOKE_DEFAULT', )
        bpy.ops.sna.steering_reset_ae4f6('INVOKE_DEFAULT', )
        bpy.context.scene.sna_rbc_control_menu.cntrl_xbox_running = False
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _FE555_running
        if not context.area or not _FE555_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.window.cursor_set('DEFAULT')
        try:
            RBWSpeed = bpy.context.scene.sna_rbw_speed
            import XInput
            CS=bpy.context.scene.sna_rbc_control_menu.carspeed
            WS=bpy.context.scene.sna_rbc_control_menu.worldspeed
            on=bpy.types.FunctionNodeInputBool
            rig=bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers
            state=XInput.get_state(0)
            if XInput.get_connected():
                on = True
            else:
                on = False
            rig.steering = XInput.get_thumb_values(state)[0][0]
            rig.target_speed = XInput.get_trigger_values(state)[1]*CS
            if XInput.get_trigger_values(state)[0]:
                 rig.target_speed = XInput.get_trigger_values(state)[0]*-CS
            rig.brake = 0
            if XInput.get_button_values(state)['X']:
                rig.brake = 1
            if XInput.get_button_values(state)['START']:
                 bpy.ops.screen.animation_play()
             #SlowMo           
            elif XInput.get_button_values(state)['A']:
                bpy.context.scene.rigidbody_world.time_scale = WS
            else:
                bpy.context.scene.rigidbody_world.time_scale = RBWSpeed
             #Reset
            if XInput.get_button_values(state)['B']:
                 bpy.ops.screen.frame_jump(end=False)
             #Save End Sim
            if XInput.get_button_values(state)['START']:
                 bpy.ops.screen.animation_play()
            #Camera
            bpy.data.objects["RBC Follow Camera"].location[0] =XInput.get_thumb_values(state)[1][0] *20
            bpy.data.objects["RBC Follow Camera"].location[2] = 7 + XInput.get_thumb_values(state)[1][1]*5
        except Exception as error:
            print(error)
        if event.type in ['RIGHTMOUSE', 'ESC']:
            self.execute(context)
            return {'CANCELLED'}
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        global _FE555_running
        if _FE555_running:
            _FE555_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            bpy.ops.sna.drive_reset_d354c('INVOKE_DEFAULT', )
            bpy.ops.sna.steering_reset_ae4f6('INVOKE_DEFAULT', )
            bpy.context.scene.sna_rbw_speed = bpy.context.scene.rigidbody_world.time_scale
            bpy.context.scene.sna_rbc_control_menu.cntrl_xbox_running = True
            bpy.ops.screen.animation_cancel('INVOKE_DEFAULT', )
            bpy.ops.screen.animation_play('INVOKE_DEFAULT', )
            context.window_manager.modal_handler_add(self)
            _FE555_running = True
            return {'RUNNING_MODAL'}


_E6557_running = False
class SNA_OT_Wasd_Modal_E6557(bpy.types.Operator):
    bl_idname = "sna.wasd_modal_e6557"
    bl_label = "WASD Modal"
    bl_description = "Starts WASD Modal Operator"
    bl_options = {"REGISTER", "UNDO"}
    cursor = "DEFAULT"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        if not False or context.area.spaces[0].bl_rna.identifier == 'SpaceView3D':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                pass
            except Exception as error:
                print(error)

    def execute(self, context):
        global _E6557_running
        _E6557_running = False
        context.window.cursor_set("DEFAULT")
        bpy.ops.screen.animation_play('INVOKE_DEFAULT', )
        bpy.context.scene.sna_rbc_control_menu.cntrl_keyboard_running = False
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.target_speed = 0.0
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.steering = 0.0
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _E6557_running
        if not context.area or not _E6557_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.window.cursor_set('DEFAULT')
        try:
            if ((event.type == 'A') and (event.value == 'PRESS')):
                bpy.context.scene.sna_rbc_control_menu.a_key_down = True
            if ((event.type == 'A') and (event.value == 'RELEASE')):
                bpy.context.scene.sna_rbc_control_menu.a_key_down = False
            if ((event.type == 'D') and (event.value == 'PRESS')):
                bpy.context.scene.sna_rbc_control_menu.d_key_down = True
            if ((event.type == 'D') and (event.value == 'RELEASE')):
                bpy.context.scene.sna_rbc_control_menu.d_key_down = False
            if ((event.type == 'W') and (event.value == 'PRESS')):
                bpy.context.scene.sna_rbc_control_menu.w_key_down = True
            if ((event.type == 'W') and (event.value == 'RELEASE')):
                bpy.context.scene.sna_rbc_control_menu.w_key_down = False
            if ((event.type == 'S') and (event.value == 'PRESS')):
                bpy.context.scene.sna_rbc_control_menu.s_key_down = True
            if ((event.type == 'S') and (event.value == 'RELEASE')):
                bpy.context.scene.sna_rbc_control_menu.s_key_down = False
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.target_speed = 0.0
            if bpy.context.scene.sna_rbc_control_menu.w_key_down:
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.target_speed = bpy.context.scene.sna_rbc_control_menu.carspeed
            if bpy.context.scene.sna_rbc_control_menu.s_key_down:
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.target_speed = float(bpy.context.scene.sna_rbc_control_menu.carspeed * -1.0)
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.steering = 0.0
            if bpy.context.scene.sna_rbc_control_menu.a_key_down:
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.steering = -1.0
            if bpy.context.scene.sna_rbc_control_menu.d_key_down:
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.steering = 1.0
            if ((event.type == 'SPACE') and (event.value == 'PRESS')):
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.brake = True
            if ((event.type == 'SPACE') and (event.value == 'RELEASE')):
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.brake = False
            if ((event.type == 'LEFT_SHIFT') and (event.value == 'PRESS')):
                bpy.context.scene.rigidbody_world.time_scale = bpy.context.scene.sna_rbc_control_menu.worldspeed
            if ((event.type == 'LEFT_SHIFT') and (event.value == 'RELEASE')):
                bpy.context.scene.rigidbody_world.time_scale = bpy.context.scene.sna_rbw_speed
            if ((event.type == 'R') and (event.value == 'PRESS')):
                bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        except Exception as error:
            print(error)
        if event.type in ['RIGHTMOUSE', 'ESC']:
            self.execute(context)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        global _E6557_running
        if _E6557_running:
            _E6557_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            bpy.context.scene.sna_rbw_speed = bpy.context.scene.rigidbody_world.time_scale
            bpy.ops.screen.animation_cancel('INVOKE_DEFAULT', )
            bpy.ops.screen.animation_play('INVOKE_DEFAULT', )
            bpy.context.scene.sna_rbc_control_menu.cntrl_keyboard_running = True
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.target_speed = 0.0
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.steering = 0.0
            if bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.brake:
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.brake = False
            context.window_manager.modal_handler_add(self)
            _E6557_running = True
            return {'RUNNING_MODAL'}


def sna_controller_panel_99B54(layout_function, input):
    if (input == 'Controller'):
        if sna_checkxinput_62230():
            col_5EA4E = layout_function.column(heading='', align=False)
            col_5EA4E.alert = False
            col_5EA4E.enabled = True
            col_5EA4E.active = True
            col_5EA4E.use_property_split = False
            col_5EA4E.use_property_decorate = False
            col_5EA4E.scale_x = 1.0
            col_5EA4E.scale_y = 1.0
            col_5EA4E.alignment = 'Expand'.upper()
            col_5EA4E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_C4114 = col_5EA4E.row(heading='', align=False)
            row_C4114.alert = False
            row_C4114.enabled = True
            row_C4114.active = True
            row_C4114.use_property_split = False
            row_C4114.use_property_decorate = False
            row_C4114.scale_x = 1.0
            row_C4114.scale_y = 1.5
            row_C4114.alignment = 'Expand'.upper()
            row_C4114.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_E3511 = row_C4114.row(heading='', align=False)
            row_E3511.alert = bpy.context.scene.sna_rbc_control_menu.cntrl_xbox_running
            row_E3511.enabled = True
            row_E3511.active = True
            row_E3511.use_property_split = False
            row_E3511.use_property_decorate = False
            row_E3511.scale_x = 1.0
            row_E3511.scale_y = 1.0
            row_E3511.alignment = 'Expand'.upper()
            row_E3511.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            op = row_E3511.operator('sna.controller_operator_fe555', text=('Stop' if bpy.context.scene.sna_rbc_control_menu.cntrl_xbox_running else 'Start'), icon_value=0, emboss=True, depress=False)
            col_5EA4E.label(text='Settings', icon_value=0)
            layout_function = col_5EA4E
            sna_advanced_keyboard_panel_BD054(layout_function, input)
            col_635C0 = col_5EA4E.column(heading='Advanced', align=False)
            col_635C0.alert = False
            col_635C0.enabled = True
            col_635C0.active = True
            col_635C0.use_property_split = False
            col_635C0.use_property_decorate = False
            col_635C0.scale_x = 1.0
            col_635C0.scale_y = 1.0
            col_635C0.alignment = 'Expand'.upper()
            col_635C0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_635C0.prop(bpy.context.scene.sna_rbc_control_menu, 'worldspeed', text='Slow Motion Speed', icon_value=0, emboss=True)
        else:
            layout_function.label(text='Run Blender as Administrator before Installing', icon_value=0)
            op = layout_function.operator('sna.import_xinput_a1516', text='Install XInput', icon_value=0, emboss=True, depress=False)


def sna_checkxinput_62230():
    Var = None
    Var = bpy.types.FunctionNodeInputBool
    try:
        import XInput
        Var=True
    except ModuleNotFoundError:
        Var=False
    return Var


class SNA_OT_Drive_Reset_D354C(bpy.types.Operator):
    bl_idname = "sna.drive_reset_d354c"
    bl_label = "Drive Reset"
    bl_description = "Resets Drive Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.target_speed = 0.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Steering_Reset_Ae4F6(bpy.types.Operator):
    bl_idname = "sna.steering_reset_ae4f6"
    bl_label = "Steering Reset"
    bl_description = "Resets Steering Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.steering = 0.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_keyboard_panel_E6220(layout_function, input):
    if 'Keyboard' in input:
        col_F5E5B = layout_function.column(heading='', align=False)
        col_F5E5B.alert = False
        col_F5E5B.enabled = True
        col_F5E5B.active = True
        col_F5E5B.use_property_split = False
        col_F5E5B.use_property_decorate = False
        col_F5E5B.scale_x = 1.0
        col_F5E5B.scale_y = 1.0
        col_F5E5B.alignment = 'Expand'.upper()
        col_F5E5B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_858A9 = col_F5E5B.column(heading='', align=False)
        col_858A9.alert = bpy.context.scene.sna_rbc_control_menu.cntrl_keyboard_running
        col_858A9.enabled = True
        col_858A9.active = True
        col_858A9.use_property_split = False
        col_858A9.use_property_decorate = False
        col_858A9.scale_x = 1.0
        col_858A9.scale_y = 1.5
        col_858A9.alignment = 'Expand'.upper()
        col_858A9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_858A9.operator('sna.wasd_modal_e6557', text=('Running... ESC or Right Click to Cancel' if bpy.context.scene.sna_rbc_control_menu.cntrl_keyboard_running else 'Start'), icon_value=0, emboss=(not bpy.context.scene.sna_rbc_control_menu.cntrl_keyboard_running), depress=False)
        col_F5E5B.label(text='Settings', icon_value=0)
        layout_function = col_F5E5B
        sna_advanced_keyboard_panel_BD054(layout_function, input)
        col_E3FD6 = col_F5E5B.column(heading='Advanced', align=False)
        col_E3FD6.alert = False
        col_E3FD6.enabled = True
        col_E3FD6.active = True
        col_E3FD6.use_property_split = False
        col_E3FD6.use_property_decorate = False
        col_E3FD6.scale_x = 1.0
        col_E3FD6.scale_y = 1.0
        col_E3FD6.alignment = 'Expand'.upper()
        col_E3FD6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_E3FD6.prop(bpy.context.scene.sna_rbc_control_menu, 'worldspeed', text='Slow Motion Speed', icon_value=0, emboss=True)


def sna_show_keyboard_maps_44FC1(layout_function, ):
    col_7A1E0 = layout_function.column(heading='', align=True)
    col_7A1E0.alert = False
    col_7A1E0.enabled = True
    col_7A1E0.active = True
    col_7A1E0.use_property_split = False
    col_7A1E0.use_property_decorate = False
    col_7A1E0.scale_x = 1.0
    col_7A1E0.scale_y = 1.0
    col_7A1E0.alignment = 'Expand'.upper()
    col_7A1E0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_7A1E0.prop(bpy.context.scene.sna_rbc_control_menu, 'controller_maps', text=('Hide Controls' if bpy.context.scene.sna_rbc_control_menu.controller_maps else 'Show Controls'), icon_value=0, emboss=True, toggle=True)
    if bpy.context.scene.sna_rbc_control_menu.controller_maps:
        box_7B3F9 = col_7A1E0.box()
        box_7B3F9.alert = False
        box_7B3F9.enabled = True
        box_7B3F9.active = True
        box_7B3F9.use_property_split = False
        box_7B3F9.use_property_decorate = False
        box_7B3F9.alignment = 'Expand'.upper()
        box_7B3F9.scale_x = 1.0
        box_7B3F9.scale_y = 1.0
        if not True: box_7B3F9.operator_context = "EXEC_DEFAULT"
        grid_B15F5 = box_7B3F9.grid_flow(columns=2, row_major=True, even_columns=True, even_rows=False, align=False)
        grid_B15F5.enabled = True
        grid_B15F5.active = True
        grid_B15F5.use_property_split = False
        grid_B15F5.use_property_decorate = True
        grid_B15F5.alignment = 'Expand'.upper()
        grid_B15F5.scale_x = 1.0
        grid_B15F5.scale_y = 1.0
        if not True: grid_B15F5.operator_context = "EXEC_DEFAULT"
        grid_B15F5.label(text='W = Drive', icon_value=0)
        grid_B15F5.label(text='S = Reverse', icon_value=0)
        grid_B15F5.label(text='A = Steer Left', icon_value=0)
        grid_B15F5.label(text='D = Steer Right', icon_value=0)
        grid_B15F5.label(text='Space_Bar = Brake', icon_value=0)
        grid_B15F5.label(text='R = Reset', icon_value=0)
        grid_B15F5.label(text='Left_Shift = Slow Motion', icon_value=0)


def sna_show_controller_maps_D3EFC(layout_function, ):
    col_EB2A3 = layout_function.column(heading='', align=True)
    col_EB2A3.alert = False
    col_EB2A3.enabled = True
    col_EB2A3.active = True
    col_EB2A3.use_property_split = False
    col_EB2A3.use_property_decorate = False
    col_EB2A3.scale_x = 1.0
    col_EB2A3.scale_y = 1.0
    col_EB2A3.alignment = 'Expand'.upper()
    col_EB2A3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_EB2A3.prop(bpy.context.scene.sna_rbc_control_menu, 'controller_maps', text=('Hide Controls' if bpy.context.scene.sna_rbc_control_menu.controller_maps else 'Show Controls'), icon_value=0, emboss=True, toggle=True)
    if bpy.context.scene.sna_rbc_control_menu.controller_maps:
        box_70F3C = col_EB2A3.box()
        box_70F3C.alert = False
        box_70F3C.enabled = True
        box_70F3C.active = True
        box_70F3C.use_property_split = False
        box_70F3C.use_property_decorate = False
        box_70F3C.alignment = 'Expand'.upper()
        box_70F3C.scale_x = 1.0
        box_70F3C.scale_y = 1.0
        if not True: box_70F3C.operator_context = "EXEC_DEFAULT"
        grid_3D64F = box_70F3C.grid_flow(columns=2, row_major=True, even_columns=True, even_rows=False, align=False)
        grid_3D64F.enabled = True
        grid_3D64F.active = True
        grid_3D64F.use_property_split = False
        grid_3D64F.use_property_decorate = True
        grid_3D64F.alignment = 'Expand'.upper()
        grid_3D64F.scale_x = 1.0
        grid_3D64F.scale_y = 1.0
        if not True: grid_3D64F.operator_context = "EXEC_DEFAULT"
        grid_3D64F.label(text='L_Trigger = Reverse', icon_value=0)
        grid_3D64F.label(text='R_Trigger = Drive', icon_value=0)
        grid_3D64F.label(text='L_Thumb Stick = Steering', icon_value=0)
        grid_3D64F.label(text='R_Thumb Stick = Camera', icon_value=0)
        grid_3D64F.label(text='X = Brake', icon_value=0)
        grid_3D64F.label(text='B = Reset', icon_value=0)
        grid_3D64F.label(text='A = Slow Motion', icon_value=0)


def sna_advanced_keyboard_panel_BD054(layout_function, input):
    if ((input == 'Keyboard') or (input == 'Controller')):
        col_C4954 = layout_function.column(heading='', align=True)
        col_C4954.alert = False
        col_C4954.enabled = True
        col_C4954.active = True
        col_C4954.use_property_split = False
        col_C4954.use_property_decorate = False
        col_C4954.scale_x = 1.0
        col_C4954.scale_y = 1.0
        col_C4954.alignment = 'Left'.upper()
        col_C4954.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_AFE4C = col_C4954.row(heading='', align=True)
        row_AFE4C.alert = False
        row_AFE4C.enabled = True
        row_AFE4C.active = True
        row_AFE4C.use_property_split = False
        row_AFE4C.use_property_decorate = False
        row_AFE4C.scale_x = 1.0
        row_AFE4C.scale_y = 1.0
        row_AFE4C.alignment = 'Expand'.upper()
        row_AFE4C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_AFE4C.prop(bpy.context.scene, 'sna_speed_unit', text=' ', icon_value=0, emboss=True, expand=True)
        box_C461B = col_C4954.box()
        box_C461B.alert = False
        box_C461B.enabled = True
        box_C461B.active = True
        box_C461B.use_property_split = False
        box_C461B.use_property_decorate = False
        box_C461B.alignment = 'Expand'.upper()
        box_C461B.scale_x = 1.0
        box_C461B.scale_y = 1.0
        if not True: box_C461B.operator_context = "EXEC_DEFAULT"
        col_E8CF6 = box_C461B.column(heading='', align=False)
        col_E8CF6.alert = False
        col_E8CF6.enabled = True
        col_E8CF6.active = True
        col_E8CF6.use_property_split = False
        col_E8CF6.use_property_decorate = False
        col_E8CF6.scale_x = 1.0
        col_E8CF6.scale_y = 1.0
        col_E8CF6.alignment = 'Expand'.upper()
        col_E8CF6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        layout_function = col_E8CF6
        sna_drive001_E6F04(layout_function, True, True, False)
        layout_function = col_E8CF6
        sna_steering001_1199D(layout_function, True, True)
        layout_function = col_E8CF6
        sna_brake001_4F195(layout_function, True, True)


def sna_drive_6B587(layout_function, input, is_target_speed):
    split_48B04 = layout_function.split(factor=0.800000011920929, align=False)
    split_48B04.alert = False
    split_48B04.enabled = True
    split_48B04.active = True
    split_48B04.use_property_split = False
    split_48B04.use_property_decorate = False
    split_48B04.scale_x = 1.0
    split_48B04.scale_y = 1.0
    split_48B04.alignment = 'Expand'.upper()
    if not True: split_48B04.operator_context = "EXEC_DEFAULT"
    col_9C41E = split_48B04.column(heading='', align=True)
    col_9C41E.alert = False
    col_9C41E.enabled = True
    col_9C41E.active = True
    col_9C41E.use_property_split = False
    col_9C41E.use_property_decorate = False
    col_9C41E.scale_x = 1.0
    col_9C41E.scale_y = 1.0
    col_9C41E.alignment = 'Expand'.upper()
    col_9C41E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if is_target_speed:
        col_9C41E.prop(bpy.context.scene.sna_rbc_control_menu, 'carspeed', text='Speed', icon_value=0, emboss=True)
    else:
        col_9C41E.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'target_speed', text='Speed', icon_value=0, emboss=True)
    if input:
        col_FAAF7 = col_9C41E.column(heading='', align=True)
        col_FAAF7.alert = False
        col_FAAF7.enabled = True
        col_FAAF7.active = True
        col_FAAF7.use_property_split = False
        col_FAAF7.use_property_decorate = False
        col_FAAF7.scale_x = 1.0
        col_FAAF7.scale_y = 1.0
        col_FAAF7.alignment = 'Expand'.upper()
        col_FAAF7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_FAAF7.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'time', text='Time', icon_value=0, emboss=True, slider=False)
        col_FAAF7.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'torque', text='Torque', icon_value=0, emboss=True)
    row_0DCD3 = split_48B04.row(heading='', align=True)
    row_0DCD3.alert = False
    row_0DCD3.enabled = True
    row_0DCD3.active = True
    row_0DCD3.use_property_split = False
    row_0DCD3.use_property_decorate = False
    row_0DCD3.scale_x = 2.0
    row_0DCD3.scale_y = 1.0
    row_0DCD3.alignment = 'Expand'.upper()
    row_0DCD3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = row_0DCD3.operator('sna.drive_reset_d354c', text='', icon_value=715, emboss=True, depress=False)
    row_0DCD3.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'disable_drive', text='', icon_value=3, emboss=True)


def sna_brake_668FB(layout_function, input, disable):
    split_B5C4F = layout_function.split(factor=0.7990646362304688, align=False)
    split_B5C4F.alert = False
    split_B5C4F.enabled = True
    split_B5C4F.active = True
    split_B5C4F.use_property_split = True
    split_B5C4F.use_property_decorate = False
    split_B5C4F.scale_x = 1.0
    split_B5C4F.scale_y = 1.0
    split_B5C4F.alignment = 'Expand'.upper()
    if not True: split_B5C4F.operator_context = "EXEC_DEFAULT"
    col_B000B = split_B5C4F.column(heading='', align=True)
    col_B000B.alert = False
    col_B000B.enabled = True
    col_B000B.active = True
    col_B000B.use_property_split = False
    col_B000B.use_property_decorate = False
    col_B000B.scale_x = 1.0
    col_B000B.scale_y = 1.0
    col_B000B.alignment = 'Expand'.upper()
    col_B000B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_8CF85 = col_B000B.row(heading='', align=True)
    row_8CF85.alert = False
    row_8CF85.enabled = (not disable)
    row_8CF85.active = True
    row_8CF85.use_property_split = False
    row_8CF85.use_property_decorate = False
    row_8CF85.scale_x = 1.0
    row_8CF85.scale_y = 1.0
    row_8CF85.alignment = 'Expand'.upper()
    row_8CF85.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_8CF85.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'brake', text='Brake', icon_value=0, emboss=True, toggle=True)
    col_D4D00 = col_B000B.column(heading='', align=True)
    col_D4D00.alert = False
    col_D4D00.enabled = True
    col_D4D00.active = True
    col_D4D00.use_property_split = False
    col_D4D00.use_property_decorate = False
    col_D4D00.scale_x = 1.0
    col_D4D00.scale_y = 1.0
    col_D4D00.alignment = 'Expand'.upper()
    col_D4D00.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if input:
        col_D4D00.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'brake_strength', text='Brake Strength', icon_value=0, emboss=True, slider=True)
    split_B5C4F.label(text='', icon_value=0)


def sna_steering_B1C34(layout_function, input, disable):
    split_44873 = layout_function.split(factor=0.800000011920929, align=False)
    split_44873.alert = False
    split_44873.enabled = True
    split_44873.active = True
    split_44873.use_property_split = False
    split_44873.use_property_decorate = False
    split_44873.scale_x = 1.0
    split_44873.scale_y = 1.0
    split_44873.alignment = 'Expand'.upper()
    if not True: split_44873.operator_context = "EXEC_DEFAULT"
    col_12710 = split_44873.column(heading='', align=True)
    col_12710.alert = False
    col_12710.enabled = True
    col_12710.active = True
    col_12710.use_property_split = False
    col_12710.use_property_decorate = False
    col_12710.scale_x = 1.0
    col_12710.scale_y = 1.0
    col_12710.alignment = 'Expand'.upper()
    col_12710.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_A013B = col_12710.column(heading='', align=True)
    col_A013B.alert = False
    col_A013B.enabled = (not disable)
    col_A013B.active = True
    col_A013B.use_property_split = False
    col_A013B.use_property_decorate = False
    col_A013B.scale_x = 1.0
    col_A013B.scale_y = 1.0
    col_A013B.alignment = 'Expand'.upper()
    col_A013B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_A013B.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'steering', text='Steering', icon_value=0, emboss=True)
    if input:
        col_C8E48 = col_12710.column(heading='', align=True)
        col_C8E48.alert = False
        col_C8E48.enabled = True
        col_C8E48.active = True
        col_C8E48.use_property_split = False
        col_C8E48.use_property_decorate = False
        col_C8E48.scale_x = 1.0
        col_C8E48.scale_y = 1.0
        col_C8E48.alignment = 'Expand'.upper()
        col_C8E48.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_C8E48.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'steering_power', text='Steering Power', icon_value=0, emboss=True, slider=True)
    row_782F0 = split_44873.row(heading='', align=True)
    row_782F0.alert = False
    row_782F0.enabled = True
    row_782F0.active = True
    row_782F0.use_property_split = False
    row_782F0.use_property_decorate = False
    row_782F0.scale_x = 2.0
    row_782F0.scale_y = 1.0
    row_782F0.alignment = 'Expand'.upper()
    row_782F0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = row_782F0.operator('sna.steering_reset_ae4f6', text='', icon_value=715, emboss=True, depress=False)
    row_782F0.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'disable_steering', text='', icon_value=3, emboss=True)


def sna_brake001_4F195(layout_function, input, disable):
    col_70756 = layout_function.column(heading='', align=True)
    col_70756.alert = False
    col_70756.enabled = True
    col_70756.active = True
    col_70756.use_property_split = False
    col_70756.use_property_decorate = False
    col_70756.scale_x = 1.0
    col_70756.scale_y = 1.0
    col_70756.alignment = 'Expand'.upper()
    col_70756.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_72BCA = col_70756.row(heading='', align=True)
    row_72BCA.alert = False
    row_72BCA.enabled = (not disable)
    row_72BCA.active = True
    row_72BCA.use_property_split = False
    row_72BCA.use_property_decorate = False
    row_72BCA.scale_x = 1.0
    row_72BCA.scale_y = 1.0
    row_72BCA.alignment = 'Expand'.upper()
    row_72BCA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_72BCA.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'brake', text='Brake', icon_value=0, emboss=True, toggle=True)
    col_11B11 = col_70756.column(heading='', align=True)
    col_11B11.alert = False
    col_11B11.enabled = True
    col_11B11.active = True
    col_11B11.use_property_split = False
    col_11B11.use_property_decorate = False
    col_11B11.scale_x = 1.0
    col_11B11.scale_y = 1.0
    col_11B11.alignment = 'Expand'.upper()
    col_11B11.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if input:
        col_11B11.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'brake_strength', text='Brake Strength', icon_value=0, emboss=True, slider=True)


def sna_steering001_1199D(layout_function, input, disable):
    col_2ABD5 = layout_function.column(heading='', align=True)
    col_2ABD5.alert = False
    col_2ABD5.enabled = True
    col_2ABD5.active = True
    col_2ABD5.use_property_split = False
    col_2ABD5.use_property_decorate = False
    col_2ABD5.scale_x = 1.0
    col_2ABD5.scale_y = 1.0
    col_2ABD5.alignment = 'Expand'.upper()
    col_2ABD5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_6B1CA = col_2ABD5.column(heading='', align=True)
    col_6B1CA.alert = False
    col_6B1CA.enabled = (not disable)
    col_6B1CA.active = True
    col_6B1CA.use_property_split = False
    col_6B1CA.use_property_decorate = False
    col_6B1CA.scale_x = 1.0
    col_6B1CA.scale_y = 1.0
    col_6B1CA.alignment = 'Expand'.upper()
    col_6B1CA.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_6B1CA.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'steering', text='Steering', icon_value=0, emboss=True)
    if input:
        col_19F64 = col_2ABD5.column(heading='', align=True)
        col_19F64.alert = False
        col_19F64.enabled = True
        col_19F64.active = True
        col_19F64.use_property_split = False
        col_19F64.use_property_decorate = False
        col_19F64.scale_x = 1.0
        col_19F64.scale_y = 1.0
        col_19F64.alignment = 'Expand'.upper()
        col_19F64.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_19F64.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'steering_power', text='Steering Power', icon_value=0, emboss=True, slider=True)


def sna_auto_drive_6D841(layout_function, guide_prop, auto_drive):
    split_1D225 = layout_function.split(factor=0.3499999940395355, align=True)
    split_1D225.alert = False
    split_1D225.enabled = True
    split_1D225.active = True
    split_1D225.use_property_split = False
    split_1D225.use_property_decorate = False
    split_1D225.scale_x = 1.0
    split_1D225.scale_y = 1.0
    split_1D225.alignment = 'Expand'.upper()
    if not True: split_1D225.operator_context = "EXEC_DEFAULT"
    split_1D225.prop(guide_prop.rig_guide_control, 'auto_drive', text='Auto Drive', icon_value=0, emboss=True, toggle=False)
    row_44071 = split_1D225.row(heading='', align=True)
    row_44071.alert = False
    row_44071.enabled = guide_prop.rig_guide_control.auto_drive
    row_44071.active = True
    row_44071.use_property_split = False
    row_44071.use_property_decorate = False
    row_44071.scale_x = 1.0
    row_44071.scale_y = 1.0
    row_44071.alignment = 'Expand'.upper()
    row_44071.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_44071.prop(guide_prop.rig_guide_control, 'min_speed', text='Min', icon_value=0, emboss=guide_prop.rig_guide_control.auto_drive, toggle=False)
    row_44071.prop(guide_prop.rig_guide_control, 'max_speed', text='Max', icon_value=0, emboss=guide_prop.rig_guide_control.auto_drive, toggle=False)


def sna_auto_brake_6BA12(layout_function, guide_prop):
    col_6ADF1 = layout_function.column(heading='', align=False)
    col_6ADF1.alert = False
    col_6ADF1.enabled = True
    col_6ADF1.active = True
    col_6ADF1.use_property_split = False
    col_6ADF1.use_property_decorate = False
    col_6ADF1.scale_x = 1.0
    col_6ADF1.scale_y = 1.0
    col_6ADF1.alignment = 'Expand'.upper()
    col_6ADF1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    split_32C1E = col_6ADF1.split(factor=0.3499999940395355, align=True)
    split_32C1E.alert = False
    split_32C1E.enabled = True
    split_32C1E.active = True
    split_32C1E.use_property_split = False
    split_32C1E.use_property_decorate = False
    split_32C1E.scale_x = 1.0
    split_32C1E.scale_y = 1.0
    split_32C1E.alignment = 'Expand'.upper()
    if not True: split_32C1E.operator_context = "EXEC_DEFAULT"
    split_32C1E.prop(guide_prop.rig_guide_control, 'auto_brake', text='Auto Brake', icon_value=0, emboss=True, toggle=False)
    col_9358E = split_32C1E.column(heading='', align=True)
    col_9358E.alert = False
    col_9358E.enabled = guide_prop.rig_guide_control.auto_brake
    col_9358E.active = True
    col_9358E.use_property_split = False
    col_9358E.use_property_decorate = False
    col_9358E.scale_x = 1.0
    col_9358E.scale_y = 1.0
    col_9358E.alignment = 'Expand'.upper()
    col_9358E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_9358E.prop(guide_prop.rig_guide_control, 'distance', text=' Distance', icon_value=0, emboss=guide_prop.rig_guide_control.auto_brake, toggle=True)
    layout_function = col_6ADF1
    sna_brake001_4F195(layout_function, True, guide_prop.rig_guide_control.auto_brake)


def sna_auto_rreverse_A0494(layout_function, guide_prop):
    split_AEBDA = layout_function.split(factor=0.3499999940395355, align=True)
    split_AEBDA.alert = False
    split_AEBDA.enabled = True
    split_AEBDA.active = True
    split_AEBDA.use_property_split = False
    split_AEBDA.use_property_decorate = False
    split_AEBDA.scale_x = 1.0
    split_AEBDA.scale_y = 1.0
    split_AEBDA.alignment = 'Expand'.upper()
    if not True: split_AEBDA.operator_context = "EXEC_DEFAULT"
    split_AEBDA.prop(guide_prop.rig_guide_control, 'auto_reverse', text='Auto Reverse', icon_value=0, emboss=True, toggle=False)
    col_4BAD5 = split_AEBDA.column(heading='', align=True)
    col_4BAD5.alert = False
    col_4BAD5.enabled = guide_prop.rig_guide_control.auto_reverse
    col_4BAD5.active = True
    col_4BAD5.use_property_split = False
    col_4BAD5.use_property_decorate = False
    col_4BAD5.scale_x = 1.0
    col_4BAD5.scale_y = 1.0
    col_4BAD5.alignment = 'Expand'.upper()
    col_4BAD5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_4BAD5.prop(guide_prop.rig_guide_control, 'reverse_angle', text=' Angle', icon_value=0, emboss=guide_prop.rig_guide_control.auto_reverse)
    layout_function = layout_function
    sna_steering001_1199D(layout_function, True, True)


def sna_drive001_E6F04(layout_function, input, is_target_speed, disabled):
    col_B68A8 = layout_function.column(heading='', align=True)
    col_B68A8.alert = False
    col_B68A8.enabled = True
    col_B68A8.active = True
    col_B68A8.use_property_split = False
    col_B68A8.use_property_decorate = False
    col_B68A8.scale_x = 1.0
    col_B68A8.scale_y = 1.0
    col_B68A8.alignment = 'Expand'.upper()
    col_B68A8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if is_target_speed:
        col_B68A8.prop(bpy.context.scene.sna_rbc_control_menu, 'carspeed', text='Speed', icon_value=0, emboss=True)
    else:
        col_D3DDD = col_B68A8.column(heading='', align=True)
        col_D3DDD.alert = False
        col_D3DDD.enabled = (not disabled)
        col_D3DDD.active = True
        col_D3DDD.use_property_split = False
        col_D3DDD.use_property_decorate = False
        col_D3DDD.scale_x = 1.0
        col_D3DDD.scale_y = 1.0
        col_D3DDD.alignment = 'Expand'.upper()
        col_D3DDD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_D3DDD.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'target_speed', text='Speed', icon_value=0, emboss=True)
    if input:
        col_B161F = col_B68A8.column(heading='', align=True)
        col_B161F.alert = False
        col_B161F.enabled = True
        col_B161F.active = True
        col_B161F.use_property_split = False
        col_B161F.use_property_decorate = False
        col_B161F.scale_x = 1.0
        col_B161F.scale_y = 1.0
        col_B161F.alignment = 'Expand'.upper()
        col_B161F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_B161F.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'time', text='Time', icon_value=0, emboss=True, slider=False)
        col_DED0D = col_B161F.column(heading='', align=True)
        col_DED0D.alert = False
        col_DED0D.enabled = True
        col_DED0D.active = False
        col_DED0D.use_property_split = False
        col_DED0D.use_property_decorate = False
        col_DED0D.scale_x = 1.0
        col_DED0D.scale_y = 1.0
        col_DED0D.alignment = 'Expand'.upper()
        col_DED0D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_DED0D.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'drive', text='Drive', icon_value=0, emboss=True)
        col_B161F.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers, 'torque', text='Torque', icon_value=0, emboss=True)


def sna_speedometer_9C728(layout_function, ):
    col_76D2C = layout_function.column(heading='', align=True)
    col_76D2C.alert = False
    col_76D2C.enabled = True
    col_76D2C.active = True
    col_76D2C.use_property_split = False
    col_76D2C.use_property_decorate = False
    col_76D2C.scale_x = 1.0
    col_76D2C.scale_y = 1.0
    col_76D2C.alignment = 'Center'.upper()
    col_76D2C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    op = col_76D2C.operator('sna.speedometers_25082', text='Run Speedometer', icon_value=492, emboss=True, depress=bpy.context.scene.sna_speedometer_menu.run_speedometer)
    if bpy.context.scene.sna_speedometer_menu.run_speedometer:
        col_69B76 = col_76D2C.column(heading='', align=True)
        col_69B76.alert = False
        col_69B76.enabled = True
        col_69B76.active = True
        col_69B76.use_property_split = False
        col_69B76.use_property_decorate = False
        col_69B76.scale_x = 1.0
        col_69B76.scale_y = 1.0
        col_69B76.alignment = 'Center'.upper()
        col_69B76.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_D933E = col_69B76.row(heading='', align=True)
        row_D933E.alert = False
        row_D933E.enabled = True
        row_D933E.active = True
        row_D933E.use_property_split = False
        row_D933E.use_property_decorate = False
        row_D933E.scale_x = 1.0
        row_D933E.scale_y = 1.0
        row_D933E.alignment = 'Expand'.upper()
        row_D933E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_D933E.prop(bpy.context.scene.sna_speedometer_menu, 'speedometer_loc', text='X', icon_value=0, emboss=True, expand=True, index=0)
        row_D933E.prop(bpy.context.scene.sna_speedometer_menu, 'speedometer_loc', text='Y', icon_value=0, emboss=True, expand=True, index=1)
        col_69B76.prop(bpy.context.scene.sna_speedometer_menu, 'speedometer_size', text='Size', icon_value=0, emboss=True, expand=True, index=1)
        row_5BC41 = col_69B76.row(heading='', align=True)
        row_5BC41.alert = False
        row_5BC41.enabled = True
        row_5BC41.active = True
        row_5BC41.use_property_split = False
        row_5BC41.use_property_decorate = False
        row_5BC41.scale_x = 1.0
        row_5BC41.scale_y = 1.0
        row_5BC41.alignment = 'Expand'.upper()
        row_5BC41.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_5BC41.prop(bpy.context.scene.sna_speedometer_menu, 'speedometer_unit', text=' ', icon_value=0, emboss=True, expand=True)
        col_9C388 = col_69B76.column(heading='', align=True)
        col_9C388.alert = False
        col_9C388.enabled = True
        col_9C388.active = True
        col_9C388.use_property_split = False
        col_9C388.use_property_decorate = False
        col_9C388.scale_x = 1.0
        col_9C388.scale_y = 1.0
        col_9C388.alignment = 'Center'.upper()
        col_9C388.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_9C388.prop(bpy.context.scene.sna_speedometer_menu, 'speed_value', text='Speed', icon_value=0, emboss=False, expand=True)


_25082_running = False
class SNA_OT_Speedometers_25082(bpy.types.Operator):
    bl_idname = "sna.speedometers_25082"
    bl_label = "SpeedOmeters"
    bl_description = "Runs Speedometer Modal"
    bl_options = {"REGISTER", "UNDO"}
    cursor = "DEFAULT"
    _handle = None
    _event = {}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        if not True or context.area.spaces[0].bl_rna.identifier == 'SpaceView3D':
            return not False
        return False

    def save_event(self, event):
        event_options = ["type", "value", "alt", "shift", "ctrl", "oskey", "mouse_region_x", "mouse_region_y", "mouse_x", "mouse_y", "pressure", "tilt"]
        if bpy.app.version >= (3, 2, 1):
            event_options += ["type_prev", "value_prev"]
        for option in event_options: self._event[option] = getattr(event, option)

    def draw_callback_px(self, context):
        event = self._event
        if event.keys():
            event = dotdict(event)
            try:
                if bpy.context.scene.sna_speedometer_menu.speedometer_unit == "MPH":
                    font_id = 0
                    if r'' and os.path.exists(r''):
                        font_id = blf.load(r'')
                    if font_id == -1:
                        print("Couldn't load font!")
                    else:
                        x_8E357, y_8E357 = tuple(map(lambda v: int(v), tuple(mathutils.Vector((0, region_by_type(bpy.context.area, 'WINDOW').height)) + mathutils.Vector(bpy.context.scene.sna_speedometer_menu.speedometer_loc))))
                        blf.position(font_id, x_8E357, y_8E357, 0)
                        if bpy.app.version >= (3, 4, 0):
                            blf.size(font_id, bpy.context.scene.sna_speedometer_menu.speedometer_size)
                        else:
                            blf.size(font_id, bpy.context.scene.sna_speedometer_menu.speedometer_size, 72)
                        clr = (1.0, 1.0, 1.0, 1.0)
                        blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                        if 0:
                            blf.enable(font_id, blf.WORD_WRAP)
                            blf.word_wrap(font_id, 0)
                        if False:
                            blf.enable(font_id, blf.ROTATION)
                            blf.rotation(font_id, 0)
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.draw(font_id, bpy.context.scene.sna_speedometer_menu.mph)
                        blf.disable(font_id, blf.ROTATION)
                        blf.disable(font_id, blf.WORD_WRAP)
                elif bpy.context.scene.sna_speedometer_menu.speedometer_unit == "Km/h":
                    font_id = 0
                    if r'' and os.path.exists(r''):
                        font_id = blf.load(r'')
                    if font_id == -1:
                        print("Couldn't load font!")
                    else:
                        x_69000, y_69000 = tuple(map(lambda v: int(v), tuple(mathutils.Vector((0, region_by_type(bpy.context.area, 'WINDOW').height)) + mathutils.Vector(bpy.context.scene.sna_speedometer_menu.speedometer_loc))))
                        blf.position(font_id, x_69000, y_69000, 0)
                        if bpy.app.version >= (3, 4, 0):
                            blf.size(font_id, bpy.context.scene.sna_speedometer_menu.speedometer_size)
                        else:
                            blf.size(font_id, bpy.context.scene.sna_speedometer_menu.speedometer_size, 72)
                        clr = (1.0, 1.0, 1.0, 1.0)
                        blf.color(font_id, clr[0], clr[1], clr[2], clr[3])
                        if 0:
                            blf.enable(font_id, blf.WORD_WRAP)
                            blf.word_wrap(font_id, 0)
                        if False:
                            blf.enable(font_id, blf.ROTATION)
                            blf.rotation(font_id, 0)
                        blf.enable(font_id, blf.WORD_WRAP)
                        blf.draw(font_id, bpy.context.scene.sna_speedometer_menu.kmh)
                        blf.disable(font_id, blf.ROTATION)
                        blf.disable(font_id, blf.WORD_WRAP)
                else:
                    pass
            except Exception as error:
                print(error)

    def execute(self, context):
        global _25082_running
        _25082_running = False
        context.window.cursor_set("DEFAULT")
        bpy.types.SpaceView3D.draw_handler_remove(self._handle, 'WINDOW')
        bpy.context.scene.sna_speedometer_menu.run_speedometer = False
        for area in context.screen.areas:
            area.tag_redraw()
        return {"FINISHED"}

    def modal(self, context, event):
        global _25082_running
        if not context.area or not _25082_running:
            self.execute(context)
            return {'CANCELLED'}
        self.save_event(event)
        context.area.tag_redraw()
        context.window.cursor_set('DEFAULT')
        try:
            pass
        except Exception as error:
            print(error)
        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        global _25082_running
        if _25082_running:
            _25082_running = False
            return {'FINISHED'}
        else:
            self.save_event(event)
            self.start_pos = (event.mouse_x, event.mouse_y)
            bpy.context.scene.sna_speedometer_menu.run_speedometer = True
            args = (context,)
            self._handle = bpy.types.SpaceView3D.draw_handler_add(self.draw_callback_px, args, 'WINDOW', 'POST_PIXEL')
            context.window_manager.modal_handler_add(self)
            _25082_running = True
            return {'RUNNING_MODAL'}


def sna_advanced_drivers_panel_632F0(layout_function, input):
    if (input == 'Drivers'):
        col_F1B10 = layout_function.column(heading='', align=True)
        col_F1B10.alert = False
        col_F1B10.enabled = True
        col_F1B10.active = True
        col_F1B10.use_property_split = False
        col_F1B10.use_property_decorate = False
        col_F1B10.scale_x = 1.0
        col_F1B10.scale_y = 1.0
        col_F1B10.alignment = 'Expand'.upper()
        col_F1B10.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_7F48A = col_F1B10.row(heading='', align=True)
        row_7F48A.alert = False
        row_7F48A.enabled = True
        row_7F48A.active = True
        row_7F48A.use_property_split = False
        row_7F48A.use_property_decorate = False
        row_7F48A.scale_x = 1.0
        row_7F48A.scale_y = 1.0
        row_7F48A.alignment = 'Expand'.upper()
        row_7F48A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_7F48A.prop(bpy.context.scene, 'sna_speed_unit', text=' ', icon_value=0, emboss=True, expand=True)
        box_82244 = col_F1B10.box()
        box_82244.alert = False
        box_82244.enabled = True
        box_82244.active = True
        box_82244.use_property_split = False
        box_82244.use_property_decorate = False
        box_82244.alignment = 'Expand'.upper()
        box_82244.scale_x = 1.0
        box_82244.scale_y = 1.0
        if not True: box_82244.operator_context = "EXEC_DEFAULT"
        col_10C01 = box_82244.column(heading='', align=True)
        col_10C01.alert = False
        col_10C01.enabled = True
        col_10C01.active = True
        col_10C01.use_property_split = False
        col_10C01.use_property_decorate = False
        col_10C01.scale_x = 1.0
        col_10C01.scale_y = 1.0
        col_10C01.alignment = 'Left'.upper()
        col_10C01.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_DD7F5 = col_10C01.column(heading='', align=False)
        col_DD7F5.alert = False
        col_DD7F5.enabled = True
        col_DD7F5.active = True
        col_DD7F5.use_property_split = False
        col_DD7F5.use_property_decorate = False
        col_DD7F5.scale_x = 1.0
        col_DD7F5.scale_y = 1.0
        col_DD7F5.alignment = 'Expand'.upper()
        col_DD7F5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        layout_function = col_DD7F5
        sna_drive_6B587(layout_function, True, False)
        layout_function = col_DD7F5
        sna_steering_B1C34(layout_function, True, False)
        layout_function = col_DD7F5
        sna_brake_668FB(layout_function, True, False)


def sna_controls_panel_284BB(layout_function, ):
    if (len(list(bpy.context.scene.sna_rbc_rig_panel)) > 1):
        layout_function.label(text='Controls', icon_value=0)
    col_9CAF3 = layout_function.column(heading='', align=True)
    col_9CAF3.alert = False
    col_9CAF3.enabled = True
    col_9CAF3.active = True
    col_9CAF3.use_property_split = False
    col_9CAF3.use_property_decorate = False
    col_9CAF3.scale_x = 1.0
    col_9CAF3.scale_y = 1.0
    col_9CAF3.alignment = 'Expand'.upper()
    col_9CAF3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_9CAF3
    sna_fancy_rig_control_panel_BC7FE(layout_function, )
    box_494E8 = col_9CAF3.box()
    box_494E8.alert = False
    box_494E8.enabled = True
    box_494E8.active = True
    box_494E8.use_property_split = False
    box_494E8.use_property_decorate = False
    box_494E8.alignment = 'Expand'.upper()
    box_494E8.scale_x = 1.0
    box_494E8.scale_y = 1.0
    if not True: box_494E8.operator_context = "EXEC_DEFAULT"
    col_330D8 = box_494E8.column(heading='', align=True)
    col_330D8.alert = False
    col_330D8.enabled = True
    col_330D8.active = True
    col_330D8.use_property_split = False
    col_330D8.use_property_decorate = False
    col_330D8.scale_x = 1.0
    col_330D8.scale_y = 1.0
    col_330D8.alignment = 'Expand'.upper()
    col_330D8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_90FCE = col_330D8.column(heading='', align=True)
    col_90FCE.alert = False
    col_90FCE.enabled = True
    col_90FCE.active = True
    col_90FCE.use_property_split = False
    col_90FCE.use_property_decorate = False
    col_90FCE.scale_x = 1.0
    col_90FCE.scale_y = 0.10000000149011612
    col_90FCE.alignment = 'Expand'.upper()
    col_90FCE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_90FCE.label(text='', icon_value=0)
    layout_function = box_494E8
    sna_advanced_drivers_panel_632F0(layout_function, bpy.context.scene.sna_rig_control_panel)
    layout_function = box_494E8
    sna_keyboard_panel_E6220(layout_function, bpy.context.scene.sna_rig_control_panel)
    layout_function = box_494E8
    sna_controller_panel_99B54(layout_function, bpy.context.scene.sna_rig_control_panel)
    layout_function = box_494E8
    sna_guides_panel_F8509(layout_function, bpy.context.scene.sna_rig_control_panel)
    if bpy.context.scene.sna_rig_control_panel == "Controller":
        layout_function = box_494E8
        sna_show_controller_maps_D3EFC(layout_function, )
    elif bpy.context.scene.sna_rig_control_panel == "Keyboard":
        layout_function = box_494E8
        sna_show_keyboard_maps_44FC1(layout_function, )
    else:
        pass
    col_D8E0C = col_9CAF3.column(heading='', align=False)
    col_D8E0C.alert = False
    col_D8E0C.enabled = True
    col_D8E0C.active = True
    col_D8E0C.use_property_split = False
    col_D8E0C.use_property_decorate = False
    col_D8E0C.scale_x = 1.0
    col_D8E0C.scale_y = 1.0
    col_D8E0C.alignment = 'Expand'.upper()
    col_D8E0C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_42DC4 = col_D8E0C.column(heading='', align=True)
    col_42DC4.alert = False
    col_42DC4.enabled = True
    col_42DC4.active = True
    col_42DC4.use_property_split = False
    col_42DC4.use_property_decorate = False
    col_42DC4.scale_x = 1.0
    col_42DC4.scale_y = 0.10000000149011612
    col_42DC4.alignment = 'Expand'.upper()
    col_42DC4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_42DC4.label(text='', icon_value=0)
    layout_function = col_D8E0C
    sna_speedometer_9C728(layout_function, )


def sna_guides_panel_F8509(layout_function, input):
    if (input == 'Guides'):
        col_240DD = layout_function.column(heading='', align=False)
        col_240DD.alert = False
        col_240DD.enabled = True
        col_240DD.active = True
        col_240DD.use_property_split = False
        col_240DD.use_property_decorate = False
        col_240DD.scale_x = 1.0
        col_240DD.scale_y = 1.0
        col_240DD.alignment = 'Expand'.upper()
        col_240DD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_C14FB = col_240DD.column(heading='', align=False)
        col_C14FB.alert = False
        col_C14FB.enabled = True
        col_C14FB.active = True
        col_C14FB.use_property_split = False
        col_C14FB.use_property_decorate = False
        col_C14FB.scale_x = 1.0
        col_C14FB.scale_y = 1.5
        col_C14FB.alignment = 'Expand'.upper()
        col_C14FB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_C14FB.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control, 'enable_guide', text='Enable Guide', icon_value=0, emboss=True, expand=False, toggle=True)
        col_77331 = col_240DD.column(heading='', align=False)
        col_77331.alert = False
        col_77331.enabled = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.enable_guide
        col_77331.active = True
        col_77331.use_property_split = False
        col_77331.use_property_decorate = False
        col_77331.scale_x = 1.0
        col_77331.scale_y = 1.0
        col_77331.alignment = 'Expand'.upper()
        col_77331.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_9EEB0 = col_77331.column(heading='Guide Object', align=True)
        col_9EEB0.alert = False
        col_9EEB0.enabled = True
        col_9EEB0.active = True
        col_9EEB0.use_property_split = False
        col_9EEB0.use_property_decorate = False
        col_9EEB0.scale_x = 1.0
        col_9EEB0.scale_y = 1.0
        col_9EEB0.alignment = 'Center'.upper()
        col_9EEB0.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_9EEB0.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control, 'guide_object', text='', icon_value=0, emboss=True)
        col_1FBC4 = col_77331.column(heading='Guide Path', align=True)
        col_1FBC4.alert = False
        col_1FBC4.enabled = (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.guide_object != None)
        col_1FBC4.active = True
        col_1FBC4.use_property_split = False
        col_1FBC4.use_property_decorate = False
        col_1FBC4.scale_x = 1.0
        col_1FBC4.scale_y = 1.0
        col_1FBC4.alignment = 'Center'.upper()
        col_1FBC4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_1FBC4.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control, 'guide_path', text='', icon_value=0, emboss=True)
        col_1FBC4.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control, 'guide_path_distance', text='Distance', icon_value=0, emboss=True)
        if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.guide_path != None):
            col_33D15 = col_1FBC4.column(heading='', align=True)
            col_33D15.alert = False
            col_33D15.enabled = True
            col_33D15.active = True
            col_33D15.use_property_split = False
            col_33D15.use_property_decorate = False
            col_33D15.scale_x = 1.0
            col_33D15.scale_y = 1.0
            col_33D15.alignment = 'Center'.upper()
            col_33D15.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.guide_path.type == 'CURVE' and (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.guide_path.data.splines.active.type == 'BEZIER')):
                col_55AAB = col_33D15.column(heading='', align=True)
                col_55AAB.alert = False
                col_55AAB.enabled = True
                col_55AAB.active = True
                col_55AAB.use_property_split = False
                col_55AAB.use_property_decorate = False
                col_55AAB.scale_x = 1.0
                col_55AAB.scale_y = 1.0
                col_55AAB.alignment = 'Center'.upper()
                col_55AAB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_55AAB.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.guide_path.data, 'resolution_u', text='Resolution', icon_value=0, emboss=True)
            else:
                col_33D15.label(text='Select Bezier Curve Object', icon_value=2)
        layout_function = col_77331
        sna_advanced_guides_panel_CD064(layout_function, 'Guides')


def sna_rig_control_panel_enum_items(self, context):
    enum_items = [['Drivers', 'Drivers', '', 0], ['Controller', 'Controller', '', 0], ['Keyboard', 'Keyboard', '', 0], ['Guides', 'Guides', '', 0]]
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_advanced_guides_panel_CD064(layout_function, input):
    if (input == 'Guides'):
        col_4C4C2 = layout_function.column(heading='', align=True)
        col_4C4C2.alert = False
        col_4C4C2.enabled = True
        col_4C4C2.active = True
        col_4C4C2.use_property_split = False
        col_4C4C2.use_property_decorate = False
        col_4C4C2.scale_x = 1.0
        col_4C4C2.scale_y = 1.0
        col_4C4C2.alignment = 'Left'.upper()
        col_4C4C2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_23103 = col_4C4C2.column(heading='', align=True)
        col_23103.alert = False
        col_23103.enabled = (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.guide_object != None)
        col_23103.active = True
        col_23103.use_property_split = False
        col_23103.use_property_decorate = False
        col_23103.scale_x = 1.0
        col_23103.scale_y = 1.0
        col_23103.alignment = 'Left'.upper()
        col_23103.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_23103.label(text='Settings', icon_value=0)
        row_A85F8 = col_23103.row(heading='', align=True)
        row_A85F8.alert = False
        row_A85F8.enabled = True
        row_A85F8.active = True
        row_A85F8.use_property_split = False
        row_A85F8.use_property_decorate = False
        row_A85F8.scale_x = 1.0
        row_A85F8.scale_y = 1.0
        row_A85F8.alignment = 'Expand'.upper()
        row_A85F8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_A85F8.prop(bpy.context.scene, 'sna_speed_unit', text=' ', icon_value=0, emboss=True, expand=True)
        box_8DF52 = col_23103.box()
        box_8DF52.alert = False
        box_8DF52.enabled = True
        box_8DF52.active = True
        box_8DF52.use_property_split = False
        box_8DF52.use_property_decorate = False
        box_8DF52.alignment = 'Expand'.upper()
        box_8DF52.scale_x = 1.0
        box_8DF52.scale_y = 1.0
        if not True: box_8DF52.operator_context = "EXEC_DEFAULT"
        col_5093C = box_8DF52.column(heading='', align=False)
        col_5093C.alert = False
        col_5093C.enabled = True
        col_5093C.active = True
        col_5093C.use_property_split = False
        col_5093C.use_property_decorate = False
        col_5093C.scale_x = 1.0
        col_5093C.scale_y = 1.0
        col_5093C.alignment = 'Expand'.upper()
        col_5093C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        layout_function = col_5093C
        sna_auto_drive_6D841(layout_function, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig], False)
        layout_function = col_5093C
        sna_drive001_E6F04(layout_function, True, False, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_guide_control.auto_drive)
        layout_function = col_5093C
        sna_auto_rreverse_A0494(layout_function, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])
        layout_function = col_5093C
        sna_auto_brake_6BA12(layout_function, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])


@persistent
def frame_change_post_handler_9AC38(dummy):
    if (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0):
        obj = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][0].body_rb
        speed = None
        MPH = None
        KPH = None
        import mathutils
        # Get the active object
        # Get the current position of the object
        cur_pos = obj.matrix_world.translation.xy
        # Get the previous position from the object's custom properties
        prev_pos = obj.get("prev_pos")
        if prev_pos is not None:
            # Convert prev_pos to a Vector object
            prev_pos_vec = mathutils.Vector(prev_pos)
            # Calculate the linear velocity of the object
            linear_velocity = (cur_pos - prev_pos_vec.xy) * bpy.context.scene.render.fps
            # Calculate the speed in MPH
            speed = linear_velocity.length
            MPH = round(speed * 2.23694)
            KPH = round(speed * 3.6)
        # Store the current position in the object's custom properties
        obj["prev_pos"] = list(cur_pos)
        obj["speed"] = speed
        bpy.context.scene.sna_speedometer_menu.mph = str(MPH) + ' MPH'
        bpy.context.scene.sna_speedometer_menu.kmh = str(KPH) + ' Km/h'
        if ((KPH if False else MPH) != None):
            bpy.context.scene.sna_speedometer_menu.speed_value = (KPH if False else MPH)


class SNA_OT_Reset_Suspension_Limits_E12Bd(bpy.types.Operator):
    bl_idname = "sna.reset_suspension_limits_e12bd"
    bl_label = "Reset Suspension Limits"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_C5C67 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_C5C67].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_C5C67].rig_tuning_group.suspension_limits = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Spring_Stiffness_F75A8(bpy.types.Operator):
    bl_idname = "sna.reset_spring_stiffness_f75a8"
    bl_label = "Reset Spring Stiffness"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_EF42E in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_EF42E].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_EF42E].rig_tuning_group.suspension_stiffness = 50.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Spring_Damping_Ce584(bpy.types.Operator):
    bl_idname = "sna.reset_spring_damping_ce584"
    bl_label = "Reset Spring Damping"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_65A74 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_65A74].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_65A74].rig_tuning_group.suspension_damping = 2.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Motor_Torque_D3852(bpy.types.Operator):
    bl_idname = "sna.reset_motor_torque_d3852"
    bl_label = "Reset Motor Torque"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_drivers.torque = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Pivot_Points_8F3E7(bpy.types.Operator):
    bl_idname = "sna.reset_pivot_points_8f3e7"
    bl_label = "Reset Pivot Points"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_5B426 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_5B426].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_5B426].rig_tuning_group.wheels_pivot_points = 0.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Turn_Radius_B505E(bpy.types.Operator):
    bl_idname = "sna.reset_turn_radius_b505e"
    bl_label = "Reset Turn Radius"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_191CE in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_191CE].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_191CE].rig_tuning_group.wheels_turn_radius = math.radians(35.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Caster_Angle_Bbefb(bpy.types.Operator):
    bl_idname = "sna.reset_caster_angle_bbefb"
    bl_label = "Reset Caster Angle"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_E30E4 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_E30E4].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_E30E4].rig_tuning_group.wheels_camber_angle = math.radians(0.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Weight_Position_2Fbd2(bpy.types.Operator):
    bl_idname = "sna.reset_weight_position_2fbd2"
    bl_label = "Reset Weight Position"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.screen.animation_cancel('INVOKE_DEFAULT', )
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        for i_13B39 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13B39].body_tuning_button:
                if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13B39].physics_weight_position_button:
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13B39].physics_weight_position_button = False
                sna_weight_position_enabledisable_85D61(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13B39].body_rb, True, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13B39].body_model)
                bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
                sna_weight_position_enabledisable_85D61(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13B39].body_rb, False, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_13B39].body_model)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SNA_OT_Reset_Roll_Constraint_Eb720(bpy.types.Operator):
    bl_idname = "sna.reset_roll_constraint_eb720"
    bl_label = "Reset Roll Constraint"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if bpy.data.objects['Roll_Constraint'].rigid_body_constraint.enabled:
            bpy.data.objects['Roll_Constraint'].rigid_body_constraint.enabled = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Tire_Friction_A0520(bpy.types.Operator):
    bl_idname = "sna.reset_tire_friction_a0520"
    bl_label = "Reset Tire Friction"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_422E7 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_422E7].axle_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_422E7].rig_tuning_group.physics_tire_friction = 5.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Weight_3D40F(bpy.types.Operator):
    bl_idname = "sna.reset_weight_3d40f"
    bl_label = "Reset Weight"
    bl_description = "Resets to Default Value"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_BF324 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
            if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_BF324].body_tuning_button:
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_BF324].physics_weight = 1.0
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_set_rbc_wheel_E46D2(Wheel_Index):
    sna_obj_type_2568F(Wheel_Index.wheel_rb, False, None)
    Wheel_Index.wheel_model = rbc_rig_set_up_funcs['sna_rb_model']
    sna_apply_transform_B3258(Wheel_Index.wheel_rb)
    bpy.context.view_layer.objects.active = rbc_rig_set_up_funcs['sna_rb_model']
    bpy.context.view_layer.objects.active.select_set(state=True, )
    rbc_rig_set_up_funcs['sna_rb_model'] = None


def sna_set_rb_wheel_1F975(Rig_Control, RB_Wheel):
    bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
    RB_Wheel.location = bpy.context.view_layer.objects.active.location
    if (bpy.context.view_layer.objects.active.dimensions[0] > bpy.context.view_layer.objects.active.dimensions[1]):
        RB_Wheel.delta_rotation_euler = (0.0, math.radians(90.0), math.radians(90.0))
        RB_Wheel.dimensions = (bpy.context.view_layer.objects.active.dimensions[0], bpy.context.view_layer.objects.active.dimensions[2], bpy.context.view_layer.objects.active.dimensions[1])
    else:
        RB_Wheel.delta_rotation_euler = (0.0, math.radians(90.0), 0.0)
        RB_Wheel.dimensions = (bpy.context.view_layer.objects.active.dimensions[2], bpy.context.view_layer.objects.active.dimensions[1], bpy.context.view_layer.objects.active.dimensions[0])


def sna_set_car_body_8DDB3(Car_body, Control_Rig, Model):
    bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
    Car_body.location = bpy.context.view_layer.objects.active.location
    Car_body.dimensions = bpy.context.view_layer.objects.active.dimensions
    Model = bpy.context.view_layer.objects.active


def sna_reset_car_body_and_rig_76DCC(CarBody, Control_Rig):
    CarBody.location = (0.0, 0.0, 0.0)


def sna_reset_rb_any_wheel_23FEE(Index):
    Index.wheel_model = None
    Index.wheel_rb.location = (0.0, 0.0, 0.0)


def sna_obj_prep_BC366():
    bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
    bpy.ops.object.transform_apply('INVOKE_DEFAULT', location=False, rotation=True, scale=True)
    bpy.ops.object.origin_set('INVOKE_DEFAULT', type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.context.view_layer.objects.active.rotation_mode = 'XYZ'


def sna_obj_type_2568F(RB_OBJ, Is_Car_Body, Control_Rig):
    rbc_rig_set_up_funcs['sna_rb_model'] = bpy.context.view_layer.objects.active
    if bpy.context.view_layer.objects.active.type == 'EMPTY':
        bpy.context.view_layer.objects.active.select_set(state=False, )
        for i_791A6 in range(len(bpy.context.view_layer.objects.active.children)):
            bpy.context.view_layer.objects.active.children[i_791A6].select_set(state=True, )
        import bmesh
        import mathutils
        # from blender templates

        def add_box(width, height, depth):
            """
            This function takes inputs and returns vertex and face arrays.
            no actual mesh data creation is done here.
            """
            verts = [(+1.0, +1.0, -1.0),
                     (+1.0, -1.0, -1.0),
                     (-1.0, -1.0, -1.0),
                     (-1.0, +1.0, -1.0),
                     (+1.0, +1.0, +1.0),
                     (+1.0, -1.0, +1.0),
                     (-1.0, -1.0, +1.0),
                     (-1.0, +1.0, +1.0),
                     ]
            faces = [(0, 1, 2, 3),
                     (4, 7, 6, 5),
                     (0, 4, 5, 1),
                     (1, 5, 6, 2),
                     (2, 6, 7, 3),
                     (4, 0, 3, 7),
                    ]
            # apply size
            for i, v in enumerate(verts):
                verts[i] = v[0] * width, v[1] * depth, v[2] * height
            return verts, faces

        def group_bounding_box():
            minx, miny, minz = (999999.0,)*3
            maxx, maxy, maxz = (-999999.0,)*3
            location = [0.0,]*3
            for obj in bpy.context.selected_objects:
                for v in obj.bound_box:
                    v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))
                    if v_world[0] < minx:
                        minx = v_world[0]
                    if v_world[0] > maxx:
                        maxx = v_world[0]
                    if v_world[1] < miny:
                        miny = v_world[1]
                    if v_world[1] > maxy:
                        maxy = v_world[1]
                    if v_world[2] < minz:
                        minz = v_world[2]
                    if v_world[2] > maxz:
                        maxz = v_world[2]
            verts_loc, faces = add_box((maxx-minx)/2, (maxz-minz)/2, (maxy-miny)/2)
            mesh = bpy.data.meshes.new("BoundingBox")
            bm = bmesh.new()
            for v_co in verts_loc:
                bm.verts.new(v_co)
            bm.verts.ensure_lookup_table()
            for f_idx in faces:
                bm.faces.new([bm.verts[i] for i in f_idx])
            bm.to_mesh(mesh)
            mesh.update()
            location[0] = minx+((maxx-minx)/2)
            location[1] = miny+((maxy-miny)/2)
            location[2] = minz+((maxz-minz)/2)
            bbox = object_utils.object_data_add(bpy.context, mesh, operator=None)
            # does a bounding box need to display more than the bounds??
            bbox.location = location
            bbox.display_type = 'BOUNDS'
            bbox.hide_render = True
        group_bounding_box()
        if Is_Car_Body:
            sna_set_car_body_8DDB3(RB_OBJ, Control_Rig, None)
        else:
            sna_set_rb_wheel_1F975(None, RB_OBJ)
        bpy.data.meshes.remove(mesh=bpy.context.view_layer.objects.active.data, )
    else:
        sna_obj_prep_BC366()
        if Is_Car_Body:
            sna_set_car_body_8DDB3(RB_OBJ, Control_Rig, None)
        else:
            sna_set_rb_wheel_1F975(None, RB_OBJ)


def sna_apply_transform_B3258(RB_OBJ):
    bpy.context.view_layer.objects.active = RB_OBJ
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, False, False, False, False)
    RB_OBJ.select_set(state=True, )
    bpy.ops.object.transform_apply('INVOKE_DEFAULT', location=False, rotation=False, scale=True)
    bpy.context.view_layer.objects.active.select_set(state=False, )
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, False, False, False)


def sna_lock_axis_2B322(RB_OBJ, enable, Model_Prop):
    if enable:
        if (Model_Prop.dimensions[0] < Model_Prop.dimensions[1]):
            RB_OBJ.lock_location = (True, False, False)
        else:
            RB_OBJ.lock_location = (False, True, False)
    else:
        RB_OBJ.lock_location = (False, False, False)


def sna_check_if_wheel_rb_model_FA4DD():
    for i_9C8F7 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[6])):
        if (bpy.context.view_layer.objects.active == sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[6][i_9C8F7]):
            return True


def sna_checkdisable_buttons_D6DD2():
    for i_72A89 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0])):
        if (bpy.context.view_layer.objects.active == sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_72A89].wheel_model):
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[0][i_72A89].wheel_button = False
    for i_53B4C in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        if (bpy.context.view_layer.objects.active == sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_53B4C].body_model):
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_53B4C].body_button = False


def sna_clear_rbc_constraints_0AE2C(Selected_Obj):
    set_up_generate_rig['sna_clear_constraints_list'] = []
    for i_3A567 in range(len(Selected_Obj.constraints)):
        if 'RBC' in Selected_Obj.constraints[i_3A567].name:
            set_up_generate_rig['sna_clear_constraints_list'].append(Selected_Obj.constraints[i_3A567])
    for i_856EB in range(len(set_up_generate_rig['sna_clear_constraints_list'])):
        Selected_Obj.constraints.remove(constraint=set_up_generate_rig['sna_clear_constraints_list'][i_856EB], )


def sna_delete_rbc_constraint_E603C():
    for i_6B9FB in range(len(bpy.context.view_layer.objects.selected)):
        rbc_rig_set_up_funcs['sna_constraint_delete_list'] = []
        for i_6ECCE in range(len(bpy.context.view_layer.objects.selected[i_6B9FB].constraints)):
            if 'RBC' in bpy.context.view_layer.objects.selected[i_6B9FB].constraints[i_6ECCE].name:
                rbc_rig_set_up_funcs['sna_constraint_delete_list'].append(bpy.context.view_layer.objects.selected[i_6B9FB].constraints[i_6ECCE])
        for i_9EFC4 in range(len(rbc_rig_set_up_funcs['sna_constraint_delete_list'])):
            bpy.context.view_layer.objects.selected[i_6B9FB].constraints.remove(constraint=rbc_rig_set_up_funcs['sna_constraint_delete_list'][i_9EFC4], )


def sna_car_body_collection_A92C7(Car_Body, Colelction, RIg_Control, Index):
    if (None == Index.body_collection):
        Index.body_rb.location = (0.0, 0.0, 0.0)
        RIg_Control.location = (0.0, 0.0, 0.0)
        Index.body_model = None
    bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
    for i_7AF24 in range(len(Index.body_collection.objects)):
        if Index.body_collection.objects[i_7AF24].type == 'MESH':
            Index.body_collection.objects[i_7AF24].select_set(state=True, )
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
    import bmesh
    import mathutils
    # from blender templates

    def add_box(width, height, depth):
        """
        This function takes inputs and returns vertex and face arrays.
        no actual mesh data creation is done here.
        """
        verts = [(+1.0, +1.0, -1.0),
                 (+1.0, -1.0, -1.0),
                 (-1.0, -1.0, -1.0),
                 (-1.0, +1.0, -1.0),
                 (+1.0, +1.0, +1.0),
                 (+1.0, -1.0, +1.0),
                 (-1.0, -1.0, +1.0),
                 (-1.0, +1.0, +1.0),
                 ]
        faces = [(0, 1, 2, 3),
                 (4, 7, 6, 5),
                 (0, 4, 5, 1),
                 (1, 5, 6, 2),
                 (2, 6, 7, 3),
                 (4, 0, 3, 7),
                ]
        # apply size
        for i, v in enumerate(verts):
            verts[i] = v[0] * width, v[1] * depth, v[2] * height
        return verts, faces

    def group_bounding_box():
        minx, miny, minz = (999999.0,)*3
        maxx, maxy, maxz = (-999999.0,)*3
        location = [0.0,]*3
        for obj in bpy.context.selected_objects:
            for v in obj.bound_box:
                v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))
                if v_world[0] < minx:
                    minx = v_world[0]
                if v_world[0] > maxx:
                    maxx = v_world[0]
                if v_world[1] < miny:
                    miny = v_world[1]
                if v_world[1] > maxy:
                    maxy = v_world[1]
                if v_world[2] < minz:
                    minz = v_world[2]
                if v_world[2] > maxz:
                    maxz = v_world[2]
        verts_loc, faces = add_box((maxx-minx)/2, (maxz-minz)/2, (maxy-miny)/2)
        mesh = bpy.data.meshes.new("BoundingBox")
        bm = bmesh.new()
        for v_co in verts_loc:
            bm.verts.new(v_co)
        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])
        bm.to_mesh(mesh)
        mesh.update()
        location[0] = minx+((maxx-minx)/2)
        location[1] = miny+((maxy-miny)/2)
        location[2] = minz+((maxz-minz)/2)
        bbox = object_utils.object_data_add(bpy.context, mesh, operator=None)
        # does a bounding box need to display more than the bounds??
        bbox.location = location
        bbox.display_type = 'BOUNDS'
        bbox.hide_render = True
    group_bounding_box()
    Index.body_button = True
    Index.body_boundingbox = bpy.context.view_layer.objects.active
    bpy.context.view_layer.objects.active.name = Index.body_rb.name + '_BoundBox'
    sna_add_to_rig_obj_collection_31032()
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection)
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_apply_transform_B3258(Index.body_rb)


def sna_car_body_back_axle_95ABA(layout_function, car_body_prop):
    if (property_exists("car_body_prop.body_rb.sna_body_axles", globals(), locals()) and len(car_body_prop.body_rb.sna_body_axles) > 0):
        for i_60D6F in range(len(list(car_body_prop.body_rb.sna_body_axles))):
            if (i_60D6F != 0):
                if (i_60D6F != 0):
                    layout_function = layout_function
                    sna_axle_8EB1A(layout_function, list(car_body_prop.body_rb.sna_body_axles)[i_60D6F], 'B')
                else:
                    layout_function = layout_function
                    sna_axle_8EB1A(layout_function, list(car_body_prop.body_rb.sna_body_axles)[i_60D6F], 'Ba')


def sna_car_bed_axle_1437D(layout_function, car_body_prop):
    for i_64320 in range(len(car_body_prop.body_rb.sna_body_axles)):
        layout_function = layout_function
        sna_axle_8EB1A(layout_function, car_body_prop.body_rb.sna_body_axles[i_64320], 'B')


def sna_car_body_front_axle_77C63(layout_function, car_body_prop, input_001, input_002):
    if (0 == 0):
        if (property_exists("car_body_prop.body_rb.sna_body_axles", globals(), locals()) and len(car_body_prop.body_rb.sna_body_axles) > 0):
            layout_function = layout_function
            sna_axle_8EB1A(layout_function, car_body_prop.body_rb.sna_body_axles[0], 'F')


def sna_axle_8EB1A(layout_function, index, name):
    box_5D114 = layout_function.box()
    box_5D114.alert = False
    box_5D114.enabled = True
    box_5D114.active = True
    box_5D114.use_property_split = False
    box_5D114.use_property_decorate = False
    box_5D114.alignment = 'Center'.upper()
    box_5D114.scale_x = 1.0
    box_5D114.scale_y = 1.0
    if not True: box_5D114.operator_context = "EXEC_DEFAULT"
    if (property_exists("index.axle_wheels", globals(), locals()) and len(index.axle_wheels) > 0):
        if (property_exists("index.axle_wheels", globals(), locals()) and len(index.axle_wheels) > 1):
            layout_function = box_5D114
            sna_double_wheel_axle_DF3F4(layout_function, index.axle_wheels, name, index)
        else:
            layout_function = box_5D114
            sna_single_wheel_axle_4BE37(layout_function, index.axle_wheels, ('Back' if 'B' in name else 'Front'), index)


def sna_single_wheel_axle_4BE37(layout_function, wheel_collection, name, axle_index):
    col_E03CC = layout_function.column(heading='', align=True)
    col_E03CC.alert = False
    col_E03CC.enabled = True
    col_E03CC.active = True
    col_E03CC.use_property_split = False
    col_E03CC.use_property_decorate = False
    col_E03CC.scale_x = 0.699999988079071
    col_E03CC.scale_y = 1.0
    col_E03CC.alignment = 'Center'.upper()
    col_E03CC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_E03CC
    sna_wheel_button_4B968(layout_function, wheel_collection[0], name, True, False)
    if bpy.context.scene.sna_rbc_set_up_advanced.show_advanced:
        row_2F382 = col_E03CC.row(heading='', align=True)
        row_2F382.alert = False
        row_2F382.enabled = True
        row_2F382.active = True
        row_2F382.use_property_split = False
        row_2F382.use_property_decorate = False
        row_2F382.scale_x = 0.699999988079071
        row_2F382.scale_y = 2.0
        row_2F382.alignment = 'Center'.upper()
        row_2F382.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_2F382.prop(axle_index, 'axle_type', text='', icon_value=0, emboss=True)


def sna_wheel_button_4B968(layout_function, index, name, show_add_button, buttons_r_side):
    col_89901 = layout_function.column(heading='', align=True)
    col_89901.alert = False
    col_89901.enabled = True
    col_89901.active = True
    col_89901.use_property_split = False
    col_89901.use_property_decorate = False
    col_89901.scale_x = 1.0
    col_89901.scale_y = 1.0
    col_89901.alignment = 'Center'.upper()
    col_89901.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_93986 = col_89901.row(heading='', align=False)
    row_93986.alert = False
    row_93986.enabled = True
    row_93986.active = True
    row_93986.use_property_split = False
    row_93986.use_property_decorate = False
    row_93986.scale_x = 1.5
    row_93986.scale_y = 5.0
    row_93986.alignment = 'Center'.upper()
    row_93986.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if property_exists("index", globals(), locals()):
        col_0054D = row_93986.column(heading='', align=True)
        col_0054D.alert = False
        col_0054D.enabled = True
        col_0054D.active = True
        col_0054D.use_property_split = False
        col_0054D.use_property_decorate = False
        col_0054D.scale_x = 1.0
        col_0054D.scale_y = 1.0
        col_0054D.alignment = 'Center'.upper()
        col_0054D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_0AFBB = col_0054D.column(heading='', align=True)
        col_0AFBB.alert = False
        col_0AFBB.enabled = True
        col_0AFBB.active = True
        col_0AFBB.use_property_split = False
        col_0AFBB.use_property_decorate = False
        col_0AFBB.scale_x = 1.0
        col_0AFBB.scale_y = (0.6499999761581421 if bpy.context.scene.sna_rbc_set_up_advanced.show_collections else 1.0)
        col_0AFBB.alignment = 'Center'.upper()
        col_0AFBB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if bpy.context.scene.sna_rbc_set_up_advanced.show_add_button:
            if buttons_r_side:
                col_58D0B = col_0AFBB.column(heading='', align=True)
                col_58D0B.alert = False
                col_58D0B.enabled = True
                col_58D0B.active = True
                col_58D0B.use_property_split = False
                col_58D0B.use_property_decorate = False
                col_58D0B.scale_x = 1.0
                col_58D0B.scale_y = 1.0
                col_58D0B.alignment = 'Center'.upper()
                col_58D0B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                split_BFD75 = col_58D0B.split(factor=0.699999988079071, align=True)
                split_BFD75.alert = False
                split_BFD75.enabled = True
                split_BFD75.active = True
                split_BFD75.use_property_split = False
                split_BFD75.use_property_decorate = False
                split_BFD75.scale_x = 0.7200000286102295
                split_BFD75.scale_y = 1.0
                split_BFD75.alignment = 'Center'.upper()
                if not True: split_BFD75.operator_context = "EXEC_DEFAULT"
                col_21FBF = split_BFD75.column(heading='', align=True)
                col_21FBF.alert = False
                col_21FBF.enabled = (not bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged)
                col_21FBF.active = True
                col_21FBF.use_property_split = False
                col_21FBF.use_property_decorate = False
                col_21FBF.scale_x = 1.0
                col_21FBF.scale_y = 1.0
                col_21FBF.alignment = 'Center'.upper()
                col_21FBF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_21FBF.prop(index, 'wheel_button', text=name, icon_value=0, emboss=True, toggle=True)
                col_4B304 = split_BFD75.column(heading='', align=True)
                col_4B304.alert = False
                col_4B304.enabled = (index.wheel_button and (sna_check_if_wheel_rb_model_FA4DD() == None))
                col_4B304.active = True
                col_4B304.use_property_split = False
                col_4B304.use_property_decorate = False
                col_4B304.scale_x = 1.0
                col_4B304.scale_y = 1.0
                col_4B304.alignment = 'Center'.upper()
                col_4B304.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_4B304.prop(index, 'wheel_extra_button', text='', icon_value=(33 if index.wheel_extra_button else 9), emboss=True, toggle=True)
            else:
                split_B5EDD = col_0AFBB.split(factor=0.30000001192092896, align=True)
                split_B5EDD.alert = False
                split_B5EDD.enabled = True
                split_B5EDD.active = True
                split_B5EDD.use_property_split = False
                split_B5EDD.use_property_decorate = False
                split_B5EDD.scale_x = 0.7200000286102295
                split_B5EDD.scale_y = 1.0
                split_B5EDD.alignment = 'Center'.upper()
                if not True: split_B5EDD.operator_context = "EXEC_DEFAULT"
                col_0E7A3 = split_B5EDD.column(heading='', align=True)
                col_0E7A3.alert = False
                col_0E7A3.enabled = (index.wheel_button and (sna_check_if_wheel_rb_model_FA4DD() == None))
                col_0E7A3.active = True
                col_0E7A3.use_property_split = False
                col_0E7A3.use_property_decorate = False
                col_0E7A3.scale_x = 1.0
                col_0E7A3.scale_y = 1.0
                col_0E7A3.alignment = 'Center'.upper()
                col_0E7A3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_0E7A3.prop(index, 'wheel_extra_button', text='', icon_value=(33 if index.wheel_extra_button else 9), emboss=True, toggle=True)
                col_2143B = split_B5EDD.column(heading='', align=True)
                col_2143B.alert = False
                col_2143B.enabled = (not bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged)
                col_2143B.active = True
                col_2143B.use_property_split = False
                col_2143B.use_property_decorate = False
                col_2143B.scale_x = 1.0199999809265137
                col_2143B.scale_y = 1.0
                col_2143B.alignment = 'Center'.upper()
                col_2143B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
                col_2143B.prop(index, 'wheel_button', text=name, icon_value=0, emboss=True, toggle=True)
        else:
            col_FBBCE = col_0AFBB.column(heading='', align=True)
            col_FBBCE.alert = False
            col_FBBCE.enabled = (not bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged)
            col_FBBCE.active = True
            col_FBBCE.use_property_split = False
            col_FBBCE.use_property_decorate = False
            col_FBBCE.scale_x = 1.1100000143051147
            col_FBBCE.scale_y = 1.0
            col_FBBCE.alignment = 'Center'.upper()
            col_FBBCE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_FBBCE.prop(index, 'wheel_button', text=name, icon_value=0, emboss=True, toggle=True)
        col_7F856 = col_0054D.column(heading='', align=True)
        col_7F856.alert = False
        col_7F856.enabled = (not bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged)
        col_7F856.active = True
        col_7F856.use_property_split = False
        col_7F856.use_property_decorate = False
        col_7F856.scale_x = 0.25999999046325684
        col_7F856.scale_y = 0.5
        col_7F856.alignment = 'Center'.upper()
        col_7F856.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if bpy.context.scene.sna_rbc_set_up_advanced.show_collections:
            col_2DAE5 = col_7F856.column(heading='', align=True)
            col_2DAE5.alert = False
            col_2DAE5.enabled = True
            col_2DAE5.active = True
            col_2DAE5.use_property_split = False
            col_2DAE5.use_property_decorate = False
            col_2DAE5.scale_x = 1.0
            col_2DAE5.scale_y = 0.75
            col_2DAE5.alignment = 'Center'.upper()
            col_2DAE5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_2DAE5.prop(index, 'wheel_collection', text='', icon_value=0, emboss=True)


def sna_advanced_set_up_panel_107AA(layout_function, ):
    if 'Set Up' in str(list(bpy.context.scene.sna_rbc_rig_panel)):
        col_058D4 = layout_function.column(heading='', align=True)
        col_058D4.alert = False
        col_058D4.enabled = True
        col_058D4.active = True
        col_058D4.use_property_split = False
        col_058D4.use_property_decorate = False
        col_058D4.scale_x = 1.0
        col_058D4.scale_y = 1.0
        col_058D4.alignment = 'Expand'.upper()
        col_058D4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_058D4.prop(bpy.context.scene.sna_rbc_set_up_advanced, 'show_advanced', text='Axles', icon_value=0, emboss=True, expand=False, toggle=True, index=3)
        grid_38011 = col_058D4.grid_flow(columns=6, row_major=False, even_columns=False, even_rows=False, align=True)
        grid_38011.enabled = True
        grid_38011.active = True
        grid_38011.use_property_split = False
        grid_38011.use_property_decorate = False
        grid_38011.alignment = 'Expand'.upper()
        grid_38011.scale_x = 1.0
        grid_38011.scale_y = 1.0
        if not True: grid_38011.operator_context = "EXEC_DEFAULT"
        grid_38011.prop(bpy.context.scene.sna_rbc_set_up_advanced, 'show_collections', text='Collections', icon_value=0, emboss=True, expand=False, toggle=True, index=3)
        grid_38011.prop(bpy.context.scene.sna_rbc_set_up_advanced, 'show_add_button', text='Extra', icon_value=0, emboss=True, expand=False, toggle=True, index=3)


def sna_double_wheel_axle_DF3F4(layout_function, wheel_collection, name, axle_index):
    row_CA283 = layout_function.row(heading='', align=True)
    row_CA283.alert = False
    row_CA283.enabled = True
    row_CA283.active = True
    row_CA283.use_property_split = False
    row_CA283.use_property_decorate = False
    row_CA283.scale_x = 1.0
    row_CA283.scale_y = 1.0
    row_CA283.alignment = 'Center'.upper()
    row_CA283.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_F65A5 = row_CA283.row(heading='', align=True)
    row_F65A5.alert = False
    row_F65A5.enabled = True
    row_F65A5.active = True
    row_F65A5.use_property_split = False
    row_F65A5.use_property_decorate = False
    row_F65A5.scale_x = 1.0
    row_F65A5.scale_y = 1.0
    row_F65A5.alignment = 'Expand'.upper()
    row_F65A5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = row_F65A5
    sna_wheel_button_4B968(layout_function, wheel_collection[1], name + 'L', False, False)
    col_964C6 = row_CA283.column(heading='', align=True)
    col_964C6.alert = False
    col_964C6.enabled = True
    col_964C6.active = True
    col_964C6.use_property_split = False
    col_964C6.use_property_decorate = False
    col_964C6.scale_x = 0.8199999928474426
    col_964C6.scale_y = 2.0
    col_964C6.alignment = 'Expand'.upper()
    col_964C6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_598B7 = col_964C6.column(heading='', align=True)
    col_598B7.alert = False
    col_598B7.enabled = True
    col_598B7.active = True
    col_598B7.use_property_split = False
    col_598B7.use_property_decorate = False
    col_598B7.scale_x = 1.0
    col_598B7.scale_y = 0.699999988079071
    col_598B7.alignment = 'Center'.upper()
    col_598B7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_598B7.label(text='', icon_value=0)
    if bpy.context.scene.sna_rbc_set_up_advanced.show_advanced:
        col_964C6.prop(axle_index, 'axle_type', text='', icon_value=0, emboss=True)
    else:
        box_75C87 = col_964C6.box()
        box_75C87.alert = False
        box_75C87.enabled = True
        box_75C87.active = True
        box_75C87.use_property_split = False
        box_75C87.use_property_decorate = False
        box_75C87.alignment = 'Center'.upper()
        box_75C87.scale_x = 2.7749998569488525
        box_75C87.scale_y = 0.7300002574920654
        if not True: box_75C87.operator_context = "EXEC_DEFAULT"
        box_75C87.label(text='', icon_value=0)
    layout_function = row_CA283
    sna_wheel_button_4B968(layout_function, wheel_collection[0], name + 'R', False, True)


def sna_set_up_panel_DACC3(layout_function, ):
    if (len(list(bpy.context.scene.sna_rbc_rig_panel)) > 1):
        layout_function.label(text='Set Up', icon_value=0)
    col_A4D72 = layout_function.column(heading='', align=True)
    col_A4D72.alert = False
    col_A4D72.enabled = True
    col_A4D72.active = True
    col_A4D72.use_property_split = False
    col_A4D72.use_property_decorate = False
    col_A4D72.scale_x = 1.0
    col_A4D72.scale_y = 1.0
    col_A4D72.alignment = 'Expand'.upper()
    col_A4D72.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if (bpy.context.view_layer.objects.active != None):
        col_ACACE = col_A4D72.column(heading='', align=True)
        col_ACACE.alert = True
        col_ACACE.enabled = True
        col_ACACE.active = True
        col_ACACE.use_property_split = False
        col_ACACE.use_property_decorate = False
        col_ACACE.scale_x = 1.0
        col_ACACE.scale_y = 1.0
        col_ACACE.alignment = 'Expand'.upper()
        col_ACACE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if ((bpy.context.view_layer.objects.active.delta_location[0], bpy.context.view_layer.objects.active.delta_location[1], bpy.context.view_layer.objects.active.delta_location[2]) != (0.0, 0.0, 0.0)):
            col_ACACE.label(text='Selected object has Delta Transforms:', icon_value=2)
            col_ACACE.label(text='        Apply Delta Transforms to Location', icon_value=0)
        if property_exists("bpy.context.object.data.users", globals(), locals()):
            if (bpy.context.object.data.users > 1):
                col_ACACE.label(text='Selected object data has multiple users:', icon_value=2)
                col_ACACE.label(text='        Make Object & Data single user', icon_value=0)
    layout_function = col_A4D72
    sna_advanced_set_up_panel_107AA(layout_function, )
    layout_function = col_A4D72
    sna_rig_set_up_D63DF(layout_function, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])
    if bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_rbc_collection_list].rig_rigged:
        col_BEBEC = col_A4D72.column(heading='', align=True)
        col_BEBEC.alert = True
        col_BEBEC.enabled = True
        col_BEBEC.active = True
        col_BEBEC.use_property_split = False
        col_BEBEC.use_property_decorate = False
        col_BEBEC.scale_x = 1.0
        col_BEBEC.scale_y = 2.25
        col_BEBEC.alignment = 'Expand'.upper()
        col_BEBEC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_BEBEC.operator('sna.clear_rig_4ed9b', text='Clear Rig', icon_value=0, emboss=True, depress=False)
    else:
        col_53880 = col_A4D72.column(heading='', align=True)
        col_53880.alert = False
        col_53880.enabled = sna_enable_generate_button_C50DB()
        col_53880.active = True
        col_53880.use_property_split = False
        col_53880.use_property_decorate = False
        col_53880.scale_x = 1.0
        col_53880.scale_y = 2.25
        col_53880.alignment = 'Expand'.upper()
        col_53880.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = col_53880.operator('sna.generate_rig_6c502', text='Generate Rig', icon_value=0, emboss=True, depress=False)


def sna_rig_set_up_D63DF(layout_function, index):
    col_B8771 = layout_function.column(heading='', align=True)
    col_B8771.alert = False
    col_B8771.enabled = True
    col_B8771.active = True
    col_B8771.use_property_split = False
    col_B8771.use_property_decorate = False
    col_B8771.scale_x = 0.699999988079071
    col_B8771.scale_y = 0.699999988079071
    col_B8771.alignment = 'Center'.upper()
    col_B8771.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_B8771
    sna_car_body__0E1B8(layout_function, index.rig_bodies)


def sna_car_body__0E1B8(layout_function, car_body_prop):
    for i_9256F in range(len(car_body_prop)):
        if (i_9256F == 0):
            col_FC767 = layout_function.column(heading='', align=True)
            col_FC767.alert = False
            col_FC767.enabled = True
            col_FC767.active = True
            col_FC767.use_property_split = False
            col_FC767.use_property_decorate = False
            col_FC767.scale_x = 1.0
            col_FC767.scale_y = 1.0
            col_FC767.alignment = 'Center'.upper()
            col_FC767.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            layout_function = col_FC767
            sna_car_body_front_axle_77C63(layout_function, car_body_prop[i_9256F], None, None)
            layout_function = col_FC767
            sna_car_body_button_8D9ED(layout_function, car_body_prop[i_9256F], car_body_prop[i_9256F].name)
            layout_function = col_FC767
            sna_car_body_back_axle_95ABA(layout_function, car_body_prop[i_9256F])
        else:
            col_27806 = layout_function.column(heading='', align=True)
            col_27806.alert = False
            col_27806.enabled = True
            col_27806.active = True
            col_27806.use_property_split = False
            col_27806.use_property_decorate = False
            col_27806.scale_x = 1.0
            col_27806.scale_y = 1.0
            col_27806.alignment = 'Center'.upper()
            col_27806.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            col_CDCD4 = col_27806.column(heading='', align=True)
            col_CDCD4.alert = False
            col_CDCD4.enabled = True
            col_CDCD4.active = True
            col_CDCD4.use_property_split = False
            col_CDCD4.use_property_decorate = False
            col_CDCD4.scale_x = 1.0899999141693115
            col_CDCD4.scale_y = 0.699999988079071
            col_CDCD4.alignment = 'Center'.upper()
            col_CDCD4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            layout_function = col_CDCD4
            sna_car_body_button_8D9ED(layout_function, car_body_prop[i_9256F], car_body_prop[i_9256F].name)
            layout_function = col_27806
            sna_car_bed_axle_1437D(layout_function, car_body_prop[i_9256F])


def sna_car_body_button_8D9ED(layout_function, car_body_prop, name):
    box_88F51 = layout_function.box()
    box_88F51.alert = False
    box_88F51.enabled = True
    box_88F51.active = True
    box_88F51.use_property_split = False
    box_88F51.use_property_decorate = False
    box_88F51.alignment = 'Center'.upper()
    box_88F51.scale_x = 1.25
    box_88F51.scale_y = 1.25
    if not True: box_88F51.operator_context = "EXEC_DEFAULT"
    row_8D166 = box_88F51.row(heading='', align=True)
    row_8D166.alert = False
    row_8D166.enabled = True
    row_8D166.active = True
    row_8D166.use_property_split = False
    row_8D166.use_property_decorate = False
    row_8D166.scale_x = 1.0
    row_8D166.scale_y = 1.0
    row_8D166.alignment = 'Center'.upper()
    row_8D166.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_5F4E2 = row_8D166.column(heading='', align=True)
    col_5F4E2.alert = False
    col_5F4E2.enabled = True
    col_5F4E2.active = True
    col_5F4E2.use_property_split = False
    col_5F4E2.use_property_decorate = False
    col_5F4E2.scale_x = 1.0
    col_5F4E2.scale_y = 1.0
    col_5F4E2.alignment = 'Center'.upper()
    col_5F4E2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    if (car_body_prop.body_button and (not (car_body_prop.body_hitch_obj == None))):
        row_2C5E2 = col_5F4E2.row(heading='', align=True)
        row_2C5E2.alert = False
        row_2C5E2.enabled = True
        row_2C5E2.active = True
        row_2C5E2.use_property_split = False
        row_2C5E2.use_property_decorate = False
        row_2C5E2.scale_x = 1.0
        row_2C5E2.scale_y = 3.0
        row_2C5E2.alignment = 'Center'.upper()
        row_2C5E2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_2C5E2.prop(car_body_prop, 'body_hitch_button', text='H', icon_value=0, emboss=True, toggle=True)
    col_801A4 = col_5F4E2.column(heading='', align=True)
    col_801A4.alert = False
    col_801A4.enabled = (not bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged)
    col_801A4.active = True
    col_801A4.use_property_split = False
    col_801A4.use_property_decorate = False
    col_801A4.scale_x = 1.0
    col_801A4.scale_y = 5.0
    col_801A4.alignment = 'Center'.upper()
    col_801A4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_A1520 = col_801A4.column(heading='', align=True)
    col_A1520.alert = False
    col_A1520.enabled = True
    col_A1520.active = True
    col_A1520.use_property_split = False
    col_A1520.use_property_decorate = False
    col_A1520.scale_x = 1.0
    col_A1520.scale_y = (0.7300002574920654 if bpy.context.scene.sna_rbc_set_up_advanced.show_collections else 1.0)
    col_A1520.alignment = 'Center'.upper()
    col_A1520.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_A1520.prop(car_body_prop, 'body_button', text=name, icon_value=0, emboss=True, toggle=True)
    if bpy.context.scene.sna_rbc_set_up_advanced.show_collections:
        col_2DC8C = col_801A4.column(heading='', align=True)
        col_2DC8C.alert = False
        col_2DC8C.enabled = True
        col_2DC8C.active = True
        col_2DC8C.use_property_split = False
        col_2DC8C.use_property_decorate = False
        col_2DC8C.scale_x = 0.9100000858306885
        col_2DC8C.scale_y = 0.30000001192092896
        col_2DC8C.alignment = 'Center'.upper()
        col_2DC8C.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_2DC8C.prop(car_body_prop, 'body_collection', text='', icon_value=0, emboss=True)


def sna_deselect_axle_buttons_D7FAA(Value, Prop, Bool):
    if Bool:
        if Value:
            for i_8F84E in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
                if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2].index(Prop) != i_8F84E):
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_8F84E].axle_tuning_button = False


def sna_active_body_C6F79():
    for i_4809B in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_4809B].body_tuning_button:
            return sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_4809B]


def sna_deselect_body_buttons_01329(Value, Prop, Bool):
    if Bool:
        if Value:
            for i_5CEC2 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
                if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1].index(Prop) != i_5CEC2):
                    sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_5CEC2].body_tuning_button = False


def sna_activate_all_DF607(Input):
    for i_81900 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_81900].body_tuning_button = Input
    for i_88738 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_88738].axle_tuning_button = Input


def sna_active_axle_B1AAA():
    for i_3935C in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_3935C].axle_tuning_button:
            return [sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_3935C].rig_tuning_group, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_3935C], None]


def sna_check_all_FE38D():
    for i_4186F in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        for i_CC804 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
            if (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_4186F].body_tuning_button or sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_CC804].axle_tuning_button):
                return (sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_4186F].body_tuning_button or sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_CC804].axle_tuning_button)


def sna_check_axles_639EB():
    for i_64991 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_64991].axle_tuning_button:
            return sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_64991].axle_tuning_button


def sna_check_bodies_A53C2():
    for i_A6AF0 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_A6AF0].body_tuning_button:
            return sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_A6AF0].body_tuning_button


def sna_vehicle_bed_preview_28682(layout_function, prop):
    col_58632 = layout_function.column(heading='', align=True)
    col_58632.alert = False
    col_58632.enabled = True
    col_58632.active = True
    col_58632.use_property_split = False
    col_58632.use_property_decorate = False
    col_58632.scale_x = 1.0
    col_58632.scale_y = 1.0
    col_58632.alignment = 'Expand'.upper()
    col_58632.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_58632
    sna_bed_icon_button_BC263(layout_function, prop)
    layout_function = col_58632
    sna_back_axle_preview_1501E(layout_function, prop, False)


def sna_vehicle_trailer_preview_99DFA(layout_function, prop):
    col_17C3B = layout_function.column(heading='', align=True)
    col_17C3B.alert = False
    col_17C3B.enabled = True
    col_17C3B.active = True
    col_17C3B.use_property_split = False
    col_17C3B.use_property_decorate = False
    col_17C3B.scale_x = 1.0
    col_17C3B.scale_y = 1.0
    col_17C3B.alignment = 'Expand'.upper()
    col_17C3B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_17C3B
    sna_trailer_icon_button_5C20D(layout_function, prop)
    layout_function = col_17C3B
    sna_back_axle_preview_1501E(layout_function, prop, False)


def sna_vehicle_body_preview_0A716(layout_function, prop):
    col_AC1CE = layout_function.column(heading='', align=True)
    col_AC1CE.alert = False
    col_AC1CE.enabled = True
    col_AC1CE.active = True
    col_AC1CE.use_property_split = False
    col_AC1CE.use_property_decorate = False
    col_AC1CE.scale_x = 1.0
    col_AC1CE.scale_y = 1.0
    col_AC1CE.alignment = 'Expand'.upper()
    col_AC1CE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_AC1CE
    sna_front_axle_preview_40917(layout_function, prop, False)
    layout_function = col_AC1CE
    sna_body_icon_button_E6966(layout_function, prop, '')
    layout_function = col_AC1CE
    sna_back_axle_preview_1501E(layout_function, prop, True)


def sna_vehicle_body__bed_19ADF(layout_function, prop):
    col_3B91A = layout_function.column(heading='', align=True)
    col_3B91A.alert = False
    col_3B91A.enabled = True
    col_3B91A.active = True
    col_3B91A.use_property_split = False
    col_3B91A.use_property_decorate = False
    col_3B91A.scale_x = 1.0
    col_3B91A.scale_y = 1.0
    col_3B91A.alignment = 'Expand'.upper()
    col_3B91A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    layout_function = col_3B91A
    sna_vehicle_body_preview_0A716(layout_function, prop['Vehicle Body'])
    col_D867A = col_3B91A.column(heading='', align=True)
    col_D867A.alert = False
    col_D867A.enabled = True
    col_D867A.active = True
    col_D867A.use_property_split = False
    col_D867A.use_property_decorate = False
    col_D867A.scale_x = 1.0
    col_D867A.scale_y = -0.32999998331069946
    col_D867A.alignment = 'Expand'.upper()
    col_D867A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_D867A.label(text='', icon_value=0)
    layout_function = col_3B91A
    sna_vehicle_bed_preview_28682(layout_function, prop['Vehicle Bed'])


def sna_back_axle_preview_1501E(layout_function, prop, is_body):
    if is_body:
        for i_DC6C5 in range(len(prop.body_rb.sna_body_axles)):
            if (i_DC6C5 > 0):
                layout_function = layout_function
                sna_axle_icon_button_8B18B(layout_function, prop.body_rb.sna_body_axles[i_DC6C5], str(i_DC6C5))
    else:
        for i_49E35 in range(len(prop.body_rb.sna_body_axles)):
            layout_function = layout_function
            sna_axle_icon_button_8B18B(layout_function, prop.body_rb.sna_body_axles[i_49E35], str(i_49E35))


def sna_front_axle_preview_40917(layout_function, prop, is_body):
    layout_function = layout_function
    sna_axle_icon_button_8B18B(layout_function, prop.body_rb.sna_body_axles[0], '')


def sna_body_icon_button_E6966(layout_function, prop, name):
    col_AC434 = layout_function.column(heading='', align=False)
    col_AC434.alert = False
    col_AC434.enabled = True
    col_AC434.active = True
    col_AC434.use_property_split = False
    col_AC434.use_property_decorate = False
    col_AC434.scale_x = 1.0
    col_AC434.scale_y = 3.0
    col_AC434.alignment = 'Expand'.upper()
    col_AC434.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_61FE7 = col_AC434.column(heading='', align=False)
    col_61FE7.alert = False
    col_61FE7.enabled = True
    col_61FE7.active = prop.body_tuning_button
    col_61FE7.use_property_split = False
    col_61FE7.use_property_decorate = False
    col_61FE7.scale_x = 1.0
    col_61FE7.scale_y = 1.0
    col_61FE7.alignment = 'Expand'.upper()
    col_61FE7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_61FE7.prop(prop, 'body_tuning_button', text='', icon_value=0, emboss=False, toggle=True)
    col_7988A = col_61FE7.column(heading='', align=False)
    col_7988A.alert = False
    col_7988A.enabled = True
    col_7988A.active = True
    col_7988A.use_property_split = False
    col_7988A.use_property_decorate = False
    col_7988A.scale_x = 1.0
    col_7988A.scale_y = (-1.404999852180481 if property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4]['Vehicle Bed']", globals(), locals()) else -1.2549999952316284)
    col_7988A.alignment = 'Expand'.upper()
    col_7988A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_7988A.label(text='', icon_value=0)
    col_61FE7.template_icon(icon_value=(load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Bed.png')) if property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4]['Vehicle Bed']", globals(), locals()) else load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Body.png'))), scale=1.2000000476837158)
    col_6F408 = col_AC434.column(heading='', align=False)
    col_6F408.alert = False
    col_6F408.enabled = True
    col_6F408.active = True
    col_6F408.use_property_split = False
    col_6F408.use_property_decorate = False
    col_6F408.scale_x = 1.0
    col_6F408.scale_y = -0.3000001013278961
    col_6F408.alignment = 'Expand'.upper()
    col_6F408.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_6F408.label(text='', icon_value=0)


def sna_axle_icon_button_8B18B(layout_function, prop, name):
    col_3F0AB = layout_function.column(heading='', align=False)
    col_3F0AB.alert = False
    col_3F0AB.enabled = True
    col_3F0AB.active = True
    col_3F0AB.use_property_split = False
    col_3F0AB.use_property_decorate = False
    col_3F0AB.scale_x = 1.0
    col_3F0AB.scale_y = 2.0
    col_3F0AB.alignment = 'Expand'.upper()
    col_3F0AB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_F3623 = col_3F0AB.column(heading='', align=False)
    col_F3623.alert = False
    col_F3623.enabled = True
    col_F3623.active = prop.axle_tuning_button
    col_F3623.use_property_split = False
    col_F3623.use_property_decorate = False
    col_F3623.scale_x = 1.0
    col_F3623.scale_y = 1.0
    col_F3623.alignment = 'Expand'.upper()
    col_F3623.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_F3623.prop(prop, 'axle_tuning_button', text='', icon_value=0, emboss=False, toggle=True)
    col_2B518 = col_F3623.column(heading='', align=False)
    col_2B518.alert = False
    col_2B518.enabled = True
    col_2B518.active = True
    col_2B518.use_property_split = False
    col_2B518.use_property_decorate = False
    col_2B518.scale_x = 1.0
    col_2B518.scale_y = -1.850000023841858
    col_2B518.alignment = 'Expand'.upper()
    col_2B518.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_2B518.label(text='', icon_value=0)
    col_F3623.template_icon(icon_value=(load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Axle.png')) if (property_exists("prop.axle_wheels", globals(), locals()) and len(prop.axle_wheels) > 1) else load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Single.png'))), scale=2.5)
    col_76ABF = col_3F0AB.column(heading='', align=False)
    col_76ABF.alert = False
    col_76ABF.enabled = True
    col_76ABF.active = True
    col_76ABF.use_property_split = False
    col_76ABF.use_property_decorate = False
    col_76ABF.scale_x = 1.0
    col_76ABF.scale_y = -0.8100000619888306
    col_76ABF.alignment = 'Expand'.upper()
    col_76ABF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_76ABF.label(text='', icon_value=0)


def sna_bed_icon_button_BC263(layout_function, prop):
    col_E40AB = layout_function.column(heading='', align=False)
    col_E40AB.alert = False
    col_E40AB.enabled = True
    col_E40AB.active = True
    col_E40AB.use_property_split = False
    col_E40AB.use_property_decorate = False
    col_E40AB.scale_x = 1.0
    col_E40AB.scale_y = 1.5
    col_E40AB.alignment = 'Expand'.upper()
    col_E40AB.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_19D4A = col_E40AB.column(heading='', align=False)
    col_19D4A.alert = False
    col_19D4A.enabled = True
    col_19D4A.active = prop.body_tuning_button
    col_19D4A.use_property_split = False
    col_19D4A.use_property_decorate = False
    col_19D4A.scale_x = 1.0
    col_19D4A.scale_y = 1.0
    col_19D4A.alignment = 'Expand'.upper()
    col_19D4A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_19D4A.prop(prop, 'body_tuning_button', text='', icon_value=0, emboss=False, toggle=True)
    col_EF030 = col_19D4A.column(heading='', align=False)
    col_EF030.alert = False
    col_EF030.enabled = True
    col_EF030.active = True
    col_EF030.use_property_split = False
    col_EF030.use_property_decorate = False
    col_EF030.scale_x = 1.0
    col_EF030.scale_y = -2.0199999809265137
    col_EF030.alignment = 'Expand'.upper()
    col_EF030.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_EF030.label(text='', icon_value=0)
    col_19D4A.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Bed.png')), scale=2.5)
    col_79BF5 = col_E40AB.column(heading='', align=False)
    col_79BF5.alert = False
    col_79BF5.enabled = True
    col_79BF5.active = True
    col_79BF5.use_property_split = False
    col_79BF5.use_property_decorate = False
    col_79BF5.scale_x = 1.0
    col_79BF5.scale_y = -0.8999999761581421
    col_79BF5.alignment = 'Expand'.upper()
    col_79BF5.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_79BF5.label(text='', icon_value=0)


def sna_trailer_icon_button_5C20D(layout_function, prop):
    col_FF437 = layout_function.column(heading='', align=False)
    col_FF437.alert = False
    col_FF437.enabled = True
    col_FF437.active = True
    col_FF437.use_property_split = False
    col_FF437.use_property_decorate = False
    col_FF437.scale_x = 1.0
    col_FF437.scale_y = 4.449999809265137
    col_FF437.alignment = 'Expand'.upper()
    col_FF437.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_49EE9 = col_FF437.column(heading='', align=False)
    col_49EE9.alert = False
    col_49EE9.enabled = True
    col_49EE9.active = prop.body_tuning_button
    col_49EE9.use_property_split = False
    col_49EE9.use_property_decorate = False
    col_49EE9.scale_x = 1.0
    col_49EE9.scale_y = 1.0
    col_49EE9.alignment = 'Expand'.upper()
    col_49EE9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_49EE9.prop(prop, 'body_tuning_button', text='', icon_value=0, emboss=False, toggle=True)
    col_75C7B = col_49EE9.column(heading='', align=False)
    col_75C7B.alert = False
    col_75C7B.enabled = True
    col_75C7B.active = True
    col_75C7B.use_property_split = False
    col_75C7B.use_property_decorate = False
    col_75C7B.scale_x = 1.0
    col_75C7B.scale_y = -1.0399998426437378
    col_75C7B.alignment = 'Expand'.upper()
    col_75C7B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_75C7B.label(text='', icon_value=0)
    col_49EE9.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'Tuning_Preview_Trailer.png')), scale=0.6800000071525574)
    col_3E9CF = col_FF437.column(heading='', align=False)
    col_3E9CF.alert = False
    col_3E9CF.enabled = True
    col_3E9CF.active = True
    col_3E9CF.use_property_split = False
    col_3E9CF.use_property_decorate = False
    col_3E9CF.scale_x = 1.0
    col_3E9CF.scale_y = -0.1799999326467514
    col_3E9CF.alignment = 'Expand'.upper()
    col_3E9CF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_3E9CF.label(text='', icon_value=0)


def sna_tuning_preview_23687(layout_function, ):
    col_AA0BD = layout_function.column(heading='', align=True)
    col_AA0BD.alert = False
    col_AA0BD.enabled = True
    col_AA0BD.active = True
    col_AA0BD.use_property_split = False
    col_AA0BD.use_property_decorate = False
    col_AA0BD.scale_x = 1.0
    col_AA0BD.scale_y = 1.0
    col_AA0BD.alignment = 'Center'.upper()
    col_AA0BD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_34311 = col_AA0BD.row(heading='', align=True)
    row_34311.alert = False
    row_34311.enabled = True
    row_34311.active = True
    row_34311.use_property_split = False
    row_34311.use_property_decorate = False
    row_34311.scale_x = 1.0
    row_34311.scale_y = 1.0
    row_34311.alignment = 'Expand'.upper()
    row_34311.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_34311.prop(bpy.context.scene.sna_rig_tuning_menu, 'preview_selection', text=bpy.context.scene.sna_rig_tuning_menu.preview_selection, icon_value=0, emboss=True, expand=True, toggle=False, index=0)
    box_3B20C = col_AA0BD.box()
    box_3B20C.alert = False
    box_3B20C.enabled = True
    box_3B20C.active = True
    box_3B20C.use_property_split = False
    box_3B20C.use_property_decorate = False
    box_3B20C.alignment = 'Right'.upper()
    box_3B20C.scale_x = 1.0
    box_3B20C.scale_y = 0.75
    if not True: box_3B20C.operator_context = "EXEC_DEFAULT"
    box_3B20C.prop(bpy.context.scene.sna_rig_tuning_menu, 'minimize_preview', text=('Show Preview' if bpy.context.scene.sna_rig_tuning_menu.minimize_preview else 'Hide Preview'), icon_value=0, emboss=False, expand=False, toggle=False)
    if bpy.context.scene.sna_rig_tuning_menu.minimize_preview:
        pass
    else:
        col_0AD9B = col_AA0BD.column(heading='', align=True)
        col_0AD9B.alert = False
        col_0AD9B.enabled = True
        col_0AD9B.active = True
        col_0AD9B.use_property_split = False
        col_0AD9B.use_property_decorate = False
        col_0AD9B.scale_x = 1.0
        col_0AD9B.scale_y = 1.0
        col_0AD9B.alignment = 'Center'.upper()
        col_0AD9B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        box_6D6A2 = col_0AD9B.box()
        box_6D6A2.alert = False
        box_6D6A2.enabled = True
        box_6D6A2.active = True
        box_6D6A2.use_property_split = False
        box_6D6A2.use_property_decorate = False
        box_6D6A2.alignment = 'Expand'.upper()
        box_6D6A2.scale_x = 1.0
        box_6D6A2.scale_y = 1.0
        if not True: box_6D6A2.operator_context = "EXEC_DEFAULT"
        row_ED1D3 = box_6D6A2.row(heading='', align=False)
        row_ED1D3.alert = False
        row_ED1D3.enabled = True
        row_ED1D3.active = True
        row_ED1D3.use_property_split = False
        row_ED1D3.use_property_decorate = False
        row_ED1D3.scale_x = 1.0
        row_ED1D3.scale_y = 1.0
        row_ED1D3.alignment = 'Expand'.upper()
        row_ED1D3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        if (property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4]['Vehicle Body']", globals(), locals()) and property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4]['Vehicle Bed']", globals(), locals())):
            col_FE18B = row_ED1D3.column(heading='', align=True)
            col_FE18B.alert = False
            col_FE18B.enabled = True
            col_FE18B.active = True
            col_FE18B.use_property_split = False
            col_FE18B.use_property_decorate = False
            col_FE18B.scale_x = 1.0
            col_FE18B.scale_y = 1.0
            col_FE18B.alignment = 'Center'.upper()
            col_FE18B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_1A334 = col_FE18B.row(heading='', align=False)
            row_1A334.alert = False
            row_1A334.enabled = True
            row_1A334.active = True
            row_1A334.use_property_split = False
            row_1A334.use_property_decorate = False
            row_1A334.scale_x = 1.0
            row_1A334.scale_y = 1.0
            row_1A334.alignment = 'Center'.upper()
            row_1A334.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_1A334.label(text='Vehicle', icon_value=0)
            layout_function = col_FE18B
            sna_vehicle_body__bed_19ADF(layout_function, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4])
        else:
            col_D78F8 = row_ED1D3.column(heading='', align=True)
            col_D78F8.alert = False
            col_D78F8.enabled = True
            col_D78F8.active = True
            col_D78F8.use_property_split = False
            col_D78F8.use_property_decorate = False
            col_D78F8.scale_x = 1.0
            col_D78F8.scale_y = 1.0
            col_D78F8.alignment = 'Center'.upper()
            col_D78F8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_6F575 = col_D78F8.row(heading='', align=False)
            row_6F575.alert = False
            row_6F575.enabled = True
            row_6F575.active = True
            row_6F575.use_property_split = False
            row_6F575.use_property_decorate = False
            row_6F575.scale_x = 1.0
            row_6F575.scale_y = 1.0
            row_6F575.alignment = 'Center'.upper()
            row_6F575.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_6F575.label(text='Vehicle', icon_value=0)
            layout_function = col_D78F8
            sna_vehicle_body_preview_0A716(layout_function, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4]['Vehicle Body'])
        if property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4]['Vehicle Trailer']", globals(), locals()):
            col_43E30 = row_ED1D3.column(heading='', align=True)
            col_43E30.alert = False
            col_43E30.enabled = True
            col_43E30.active = True
            col_43E30.use_property_split = False
            col_43E30.use_property_decorate = False
            col_43E30.scale_x = 1.0
            col_43E30.scale_y = 1.0
            col_43E30.alignment = 'Center'.upper()
            col_43E30.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_3E39E = col_43E30.row(heading='', align=False)
            row_3E39E.alert = False
            row_3E39E.enabled = True
            row_3E39E.active = True
            row_3E39E.use_property_split = False
            row_3E39E.use_property_decorate = False
            row_3E39E.scale_x = 1.0
            row_3E39E.scale_y = 1.0
            row_3E39E.alignment = 'Center'.upper()
            row_3E39E.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
            row_3E39E.label(text='Trailer', icon_value=0)
            layout_function = col_43E30
            sna_vehicle_trailer_preview_99DFA(layout_function, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[4]['Vehicle Trailer'])


def sna_weight_position_lock_axis_4B08F(RB_OBJ, enable):
    if enable:
        if (RB_OBJ.dimensions[0] < RB_OBJ.dimensions[1]):
            RB_OBJ.lock_location = (True, False, False)
        else:
            RB_OBJ.lock_location = (False, True, False)
    else:
        RB_OBJ.lock_location = (False, False, False)


def sna_weight_position_enabledisable_85D61(RB_OBJ, enable, RB_Model_OBJ):
    bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
    sna_hide_obj_select_71598(RB_OBJ, (not enable), False, False, False)
    RB_OBJ.select_set(state=enable, )
    bpy.context.view_layer.objects.active = RB_OBJ
    bpy.context.scene.tool_settings.use_transform_data_origin = enable


def sna_drive_type_175F5(Axle_Group, Index, Front_Axle_Type, Back_Axle_Type):
    if (Index < 1):
        Axle_Group.axle_type = Front_Axle_Type
    else:
        Axle_Group.axle_type = Back_Axle_Type


def sna_reverse_drive_C54EC(Axle_Prop, Reverse_Drive):
    for i_6206A in range(len(Axle_Prop.axle_wheels)):
        if Reverse_Drive:
            Axle_Prop.axle_wheels[i_6206A].wheel_motor.delta_rotation_euler = (0.0, 0.0, math.radians(180.0))
        else:
            Axle_Prop.axle_wheels[i_6206A].wheel_motor.delta_rotation_euler = (0.0, 0.0, 0.0)


def sna_reverse_steering_38EFC(Axle_Prop, Reverse_Steering):
    for i_70A59 in range(len(Axle_Prop.axle_wheels)):
        if Reverse_Steering:
            Axle_Prop.axle_wheels[i_70A59].wheel_steeringmotor.delta_rotation_euler = (0.0, math.radians(-90.0), 0.0)
        else:
            Axle_Prop.axle_wheels[i_70A59].wheel_steeringmotor.delta_rotation_euler = (0.0, math.radians(90.0), 0.0)


def sna_show_pivot_points_A4CD7(Show, Wheel_Collection):
    for i_1B4AC in range(len(Wheel_Collection)):
        if Show:
            sna_hide_obj_select_71598(Wheel_Collection[i_1B4AC].wheel_constraint, False, False, False, False)
            Wheel_Collection[i_1B4AC].wheel_constraint.show_in_front = True
            Wheel_Collection[i_1B4AC].wheel_constraint.select_set(state=True, )
        else:
            sna_hide_obj_select_71598(Wheel_Collection[i_1B4AC].wheel_constraint, True, True, False, False)
            Wheel_Collection[i_1B4AC].wheel_constraint.show_in_front = False
            Wheel_Collection[i_1B4AC].wheel_constraint.select_set(state=False, )


def sna_show_pivot_points_select_75D30(Input):
    for i_FD54E in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2])):
        if (Input and sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_FD54E].axle_tuning_button):
            sna_show_pivot_points_A4CD7(True, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_FD54E].axle_wheels)
        else:
            sna_show_pivot_points_A4CD7(False, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[2][i_FD54E].axle_wheels)


def sna_set_weight_E58E3(OBJ, Weight_Input):
    OBJ.rigid_body.mass = float(round(eval("OBJ.dimensions[0] + OBJ.dimensions[1] + OBJ.dimensions[2] / 3"), abs(2)) * Weight_Input)
    return float(round(eval("OBJ.dimensions[0] + OBJ.dimensions[1] + OBJ.dimensions[2] / 3"), abs(2)) * Weight_Input)


@persistent
def frame_change_pre_handler_CFF48(dummy):
    if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()):
        pass


def sna_get_vehicle_weight_925DA():
    rbc_rig_tuning_funcs['sna_body_weight'] = 0.0
    rbc_rig_tuning_funcs['sna_bed_weight'] = 0.0
    rbc_rig_tuning_funcs['sna_trailer_weight'] = 0.0
    if property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][0]", globals(), locals()):
        rbc_rig_tuning_funcs['sna_body_weight'] = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][0].body_rb.rigid_body.mass
    if property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][1]", globals(), locals()):
        rbc_rig_tuning_funcs['sna_bed_weight'] = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][1].body_rb.rigid_body.mass
    if property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][2]", globals(), locals()):
        rbc_rig_tuning_funcs['sna_trailer_weight'] = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][2].body_rb.rigid_body.mass
    return float(rbc_rig_tuning_funcs['sna_body_weight'] + rbc_rig_tuning_funcs['sna_bed_weight'] + rbc_rig_tuning_funcs['sna_trailer_weight'])


def sna_update_wheel_C1773(Wheel_Prop, Is_Steering, Is_Drive, Turn_Radius):
    Wheel_Prop.wheel_constraint.rigid_body_constraint.limit_ang_z_lower = float((Turn_Radius if Is_Steering else 0.0) * -1.0)
    Wheel_Prop.wheel_constraint.rigid_body_constraint.limit_ang_z_upper = (Turn_Radius if Is_Steering else 0.0)
    Wheel_Prop.wheel_steeringmotor.rigid_body_constraint.enabled = Is_Steering
    Wheel_Prop.wheel_motor.rigid_body_constraint.enabled = Is_Drive


def sna_tuning_panel_F3327(layout_function, ):
    if (len(list(bpy.context.scene.sna_rbc_rig_panel)) > 1):
        layout_function.label(text='Tuning', icon_value=0)
    layout_function = layout_function
    sna_tuning_preview_23687(layout_function, )
    layout_function = layout_function
    sna_drive_type_35D35(layout_function, False)
    col_E07DC = layout_function.column(heading='', align=False)
    col_E07DC.alert = False
    col_E07DC.enabled = True
    col_E07DC.active = True
    col_E07DC.use_property_split = False
    col_E07DC.use_property_decorate = False
    col_E07DC.scale_x = 1.0
    col_E07DC.scale_y = 1.0
    col_E07DC.alignment = 'Expand'.upper()
    col_E07DC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_1F6C9 = col_E07DC.column(heading='', align=False)
    col_1F6C9.alert = False
    col_1F6C9.enabled = True
    col_1F6C9.active = True
    col_1F6C9.use_property_split = False
    col_1F6C9.use_property_decorate = False
    col_1F6C9.scale_x = 1.0
    col_1F6C9.scale_y = 0.5
    col_1F6C9.alignment = 'Expand'.upper()
    col_1F6C9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_1F6C9.label(text='', icon_value=0)
    col_3AB9B = col_E07DC.column(heading='', align=True)
    col_3AB9B.alert = False
    col_3AB9B.enabled = True
    col_3AB9B.active = True
    col_3AB9B.use_property_split = False
    col_3AB9B.use_property_decorate = False
    col_3AB9B.scale_x = 1.0
    col_3AB9B.scale_y = 1.0
    col_3AB9B.alignment = 'Expand'.upper()
    col_3AB9B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_246D6 = col_3AB9B.row(heading='', align=True)
    row_246D6.alert = False
    row_246D6.enabled = True
    row_246D6.active = True
    row_246D6.use_property_split = False
    row_246D6.use_property_decorate = False
    row_246D6.scale_x = 1.0
    row_246D6.scale_y = 1.149999976158142
    row_246D6.alignment = 'Expand'.upper()
    row_246D6.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_246D6.prop(bpy.context.scene, 'sna_rig_tuning_enum', text=str(list(bpy.context.scene.sna_rig_tuning_enum)), icon_value=0, emboss=True, expand=True, toggle=True)
    box_4F976 = col_3AB9B.box()
    box_4F976.alert = False
    box_4F976.enabled = True
    box_4F976.active = True
    box_4F976.use_property_split = False
    box_4F976.use_property_decorate = False
    box_4F976.alignment = 'Center'.upper()
    box_4F976.scale_x = 1.0
    box_4F976.scale_y = 1.0
    if not True: box_4F976.operator_context = "EXEC_DEFAULT"
    for i_6EB3B in range(len(sorted(list(bpy.context.scene.sna_rig_tuning_enum), reverse=True))):
        if sorted(list(bpy.context.scene.sna_rig_tuning_enum), reverse=True)[i_6EB3B] == "Wheels":
            if sna_check_axles_639EB():
                layout_function = box_4F976
                sna_wheels_92FF0(layout_function, sna_active_axle_B1AAA()[0])
        elif sorted(list(bpy.context.scene.sna_rig_tuning_enum), reverse=True)[i_6EB3B] == "Physics":
            if (sna_check_axles_639EB() or sna_check_bodies_A53C2()):
                layout_function = box_4F976
                sna_phyisics_673A2(layout_function, (not (sna_active_body_C6F79() == None)))
        elif sorted(list(bpy.context.scene.sna_rig_tuning_enum), reverse=True)[i_6EB3B] == "Suspension":
            if sna_check_axles_639EB():
                layout_function = box_4F976
                sna_suspension_85202(layout_function, sna_active_axle_B1AAA()[0])
        else:
            pass


def sna_suspension_85202(layout_function, prop):
    col_8E057 = layout_function.column(heading='', align=False)
    col_8E057.alert = False
    col_8E057.enabled = True
    col_8E057.active = True
    col_8E057.use_property_split = False
    col_8E057.use_property_decorate = False
    col_8E057.scale_x = 1.0
    col_8E057.scale_y = 1.0
    col_8E057.alignment = 'Expand'.upper()
    col_8E057.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_8E057.label(text='Suspension', icon_value=0)
    split_4D8D9 = col_8E057.split(factor=0.8999999761581421, align=False)
    split_4D8D9.alert = False
    split_4D8D9.enabled = True
    split_4D8D9.active = True
    split_4D8D9.use_property_split = False
    split_4D8D9.use_property_decorate = False
    split_4D8D9.scale_x = 1.0
    split_4D8D9.scale_y = 1.0
    split_4D8D9.alignment = 'Expand'.upper()
    if not True: split_4D8D9.operator_context = "EXEC_DEFAULT"
    split_4D8D9.prop(prop, 'suspension_limits', text='Limits', icon_value=0, emboss=True, index=0)
    op = split_4D8D9.operator('sna.reset_suspension_limits_e12bd', text='', icon_value=715, emboss=True, depress=False)
    col_D3124 = layout_function.column(heading='', align=True)
    col_D3124.alert = False
    col_D3124.enabled = True
    col_D3124.active = True
    col_D3124.use_property_split = False
    col_D3124.use_property_decorate = False
    col_D3124.scale_x = 1.0
    col_D3124.scale_y = 1.0
    col_D3124.alignment = 'Expand'.upper()
    col_D3124.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    split_8583E = col_D3124.split(factor=0.8999999761581421, align=False)
    split_8583E.alert = False
    split_8583E.enabled = True
    split_8583E.active = True
    split_8583E.use_property_split = False
    split_8583E.use_property_decorate = False
    split_8583E.scale_x = 1.0
    split_8583E.scale_y = 1.0
    split_8583E.alignment = 'Expand'.upper()
    if not True: split_8583E.operator_context = "EXEC_DEFAULT"
    split_8583E.prop(prop, 'suspension_stiffness', text='Spring Stiffness', icon_value=0, emboss=True, index=0)
    op = split_8583E.operator('sna.reset_spring_stiffness_f75a8', text='', icon_value=715, emboss=True, depress=False)
    split_90615 = col_D3124.split(factor=0.8999999761581421, align=False)
    split_90615.alert = False
    split_90615.enabled = True
    split_90615.active = True
    split_90615.use_property_split = False
    split_90615.use_property_decorate = False
    split_90615.scale_x = 1.0
    split_90615.scale_y = 1.0
    split_90615.alignment = 'Expand'.upper()
    if not True: split_90615.operator_context = "EXEC_DEFAULT"
    split_90615.prop(prop, 'suspension_damping', text='Spring Damping', icon_value=0, emboss=True, index=0)
    op = split_90615.operator('sna.reset_spring_damping_ce584', text='', icon_value=715, emboss=True, depress=False)


def sna_phyisics_673A2(layout_function, input):
    col_FD68F = layout_function.column(heading='', align=False)
    col_FD68F.alert = False
    col_FD68F.enabled = True
    col_FD68F.active = True
    col_FD68F.use_property_split = False
    col_FD68F.use_property_decorate = False
    col_FD68F.scale_x = 1.0
    col_FD68F.scale_y = 1.0
    col_FD68F.alignment = 'Expand'.upper()
    col_FD68F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_FD68F.label(text='Physics', icon_value=0)
    layout_function = col_FD68F
    sna_physics_tire_friction_4A33C(layout_function, )
    if input:
        col_0D7CE = layout_function.column(heading='', align=False)
        col_0D7CE.alert = False
        col_0D7CE.enabled = True
        col_0D7CE.active = True
        col_0D7CE.use_property_split = False
        col_0D7CE.use_property_decorate = False
        col_0D7CE.scale_x = 1.0
        col_0D7CE.scale_y = 1.0
        col_0D7CE.alignment = 'Expand'.upper()
        col_0D7CE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        layout_function = col_0D7CE
        sna_physics_weight_28844(layout_function, )
        layout_function = col_0D7CE
        sna_roll_constraints_3247F(layout_function, )


def sna_physics_weight_28844(layout_function, ):
    if (not (sna_active_body_C6F79() == None)):
        col_A7478 = layout_function.column(heading='', align=True)
        col_A7478.alert = False
        col_A7478.enabled = True
        col_A7478.active = True
        col_A7478.use_property_split = False
        col_A7478.use_property_decorate = False
        col_A7478.scale_x = 1.0
        col_A7478.scale_y = 1.0
        col_A7478.alignment = 'Expand'.upper()
        col_A7478.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split_DC36D = col_A7478.split(factor=0.8999999761581421, align=False)
        split_DC36D.alert = False
        split_DC36D.enabled = True
        split_DC36D.active = True
        split_DC36D.use_property_split = False
        split_DC36D.use_property_decorate = False
        split_DC36D.scale_x = 1.0
        split_DC36D.scale_y = 1.0
        split_DC36D.alignment = 'Expand'.upper()
        if not True: split_DC36D.operator_context = "EXEC_DEFAULT"
        split_DC36D.prop(sna_active_body_C6F79(), 'physics_weight', text='Weight', icon_value=0, emboss=True)
        op = split_DC36D.operator('sna.reset_weight_3d40f', text='', icon_value=715, emboss=True, depress=False)
        split_B62CE = col_A7478.split(factor=0.8999999761581421, align=False)
        split_B62CE.alert = False
        split_B62CE.enabled = True
        split_B62CE.active = True
        split_B62CE.use_property_split = False
        split_B62CE.use_property_decorate = False
        split_B62CE.scale_x = 1.0
        split_B62CE.scale_y = 1.0
        split_B62CE.alignment = 'Expand'.upper()
        if not True: split_B62CE.operator_context = "EXEC_DEFAULT"
        split_B62CE.prop(sna_active_body_C6F79(), 'physics_weight_position_button', text='Set Weight Position', icon_value=0, emboss=True, toggle=True)
        op = split_B62CE.operator('sna.reset_weight_position_2fbd2', text='', icon_value=715, emboss=True, depress=False)


def sna_drive_type_35D35(layout_function, input):
    box_9A88D = layout_function.box()
    box_9A88D.alert = False
    box_9A88D.enabled = True
    box_9A88D.active = True
    box_9A88D.use_property_split = False
    box_9A88D.use_property_decorate = False
    box_9A88D.alignment = 'Center'.upper()
    box_9A88D.scale_x = 1.0
    box_9A88D.scale_y = 1.0
    if not True: box_9A88D.operator_context = "EXEC_DEFAULT"
    row_1D079 = box_9A88D.row(heading='', align=True)
    row_1D079.alert = False
    row_1D079.enabled = True
    row_1D079.active = True
    row_1D079.use_property_split = False
    row_1D079.use_property_decorate = False
    row_1D079.scale_x = 1.100000023841858
    row_1D079.scale_y = 1.0
    row_1D079.alignment = 'Center'.upper()
    row_1D079.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_90119 = row_1D079.column(heading='', align=False)
    col_90119.alert = False
    col_90119.enabled = True
    col_90119.active = True
    col_90119.use_property_split = False
    col_90119.use_property_decorate = False
    col_90119.scale_x = 1.0
    col_90119.scale_y = 1.0
    col_90119.alignment = 'Center'.upper()
    col_90119.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_7D852 = col_90119.column(heading='', align=False)
    col_7D852.alert = False
    col_7D852.enabled = True
    col_7D852.active = True
    col_7D852.use_property_split = False
    col_7D852.use_property_decorate = False
    col_7D852.scale_x = 1.0
    col_7D852.scale_y = -0.3799999952316284
    col_7D852.alignment = 'Center'.upper()
    col_7D852.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_7D852.label(text='', icon_value=0)
    if 'Individual' in bpy.context.scene.sna_rig_tuning_menu.preview_selection:
        layout_function = col_90119
        sna_axle_type_selection_077D8(layout_function, )
    else:
        col_BD512 = col_90119.column(heading='', align=False)
        col_BD512.alert = False
        col_BD512.enabled = True
        col_BD512.active = True
        col_BD512.use_property_split = False
        col_BD512.use_property_decorate = False
        col_BD512.scale_x = 1.0
        col_BD512.scale_y = 1.0
        col_BD512.alignment = 'Center'.upper()
        col_BD512.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_B08CD = col_BD512.column(heading='', align=False)
        col_B08CD.alert = False
        col_B08CD.enabled = True
        col_B08CD.active = True
        col_B08CD.use_property_split = False
        col_B08CD.use_property_decorate = False
        col_B08CD.scale_x = 1.0
        col_B08CD.scale_y = 1.0
        col_B08CD.alignment = 'Center'.upper()
        col_B08CD.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_B08CD.label(text='      Drive Type', icon_value=0)
        col_BD512.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig], 'drive_type', text='', icon_value=0, emboss=True, expand=False, toggle=False)


def sna_axle_type_selection_077D8(layout_function, ):
    col_D418B = layout_function.column(heading='', align=True)
    col_D418B.alert = False
    col_D418B.enabled = True
    col_D418B.active = True
    col_D418B.use_property_split = False
    col_D418B.use_property_decorate = False
    col_D418B.scale_x = 1.0
    col_D418B.scale_y = 1.0
    col_D418B.alignment = 'Center'.upper()
    col_D418B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_2D340 = col_D418B.row(heading='', align=False)
    row_2D340.alert = False
    row_2D340.enabled = True
    row_2D340.active = True
    row_2D340.use_property_split = False
    row_2D340.use_property_decorate = False
    row_2D340.scale_x = 1.0
    row_2D340.scale_y = 1.0
    row_2D340.alignment = 'Center'.upper()
    row_2D340.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    row_2D340.label(text='Axle Type', icon_value=0)
    col_D418B.prop(sna_active_axle_B1AAA()[1], 'axle_type', text='', icon_value=0, emboss=True, expand=False, toggle=False)
    if ('Drive' in sna_active_axle_B1AAA()[1].axle_type or 'Differential' in sna_active_axle_B1AAA()[1].axle_type):
        col_D418B.prop(sna_active_axle_B1AAA()[1], 'reverse_drive', text='Reverse Drive', icon_value=0, emboss=True, expand=False, toggle=True)
    if ('Steering' in sna_active_axle_B1AAA()[1].axle_type and (not 'Differential' in sna_active_axle_B1AAA()[1].axle_type)):
        col_D418B.prop(sna_active_axle_B1AAA()[1], 'reverse_steering', text='Reverse Steering', icon_value=0, emboss=True, expand=False, toggle=True)


def sna_physics_tire_friction_4A33C(layout_function, ):
    if (not (sna_active_axle_B1AAA()[0] == None)):
        split_83B88 = layout_function.split(factor=0.8999999761581421, align=False)
        split_83B88.alert = False
        split_83B88.enabled = True
        split_83B88.active = True
        split_83B88.use_property_split = False
        split_83B88.use_property_decorate = False
        split_83B88.scale_x = 1.0
        split_83B88.scale_y = 1.0
        split_83B88.alignment = 'Expand'.upper()
        if not True: split_83B88.operator_context = "EXEC_DEFAULT"
        split_83B88.prop(sna_active_axle_B1AAA()[0], 'physics_tire_friction', text='Tire Friction', icon_value=0, emboss=True)
        op = split_83B88.operator('sna.reset_tire_friction_a0520', text='', icon_value=715, emboss=True, depress=False)


def sna_rig_tuning_enum_enum_items(self, context):
    enum_items = [['Wheels', 'Wheels', '', 567], ['Suspension', 'Suspension', '', 63], ['Physics', 'Physics', '', 89]]
    return [make_enum_item(item[0], item[1], item[2], item[3], 2**i) for i, item in enumerate(enum_items)]


def sna_wheels_92FF0(layout_function, prop):
    col_91F56 = layout_function.column(heading='', align=False)
    col_91F56.alert = False
    col_91F56.enabled = True
    col_91F56.active = True
    col_91F56.use_property_split = False
    col_91F56.use_property_decorate = False
    col_91F56.scale_x = 1.0
    col_91F56.scale_y = 1.0
    col_91F56.alignment = 'Expand'.upper()
    col_91F56.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_91F56.label(text='Wheels', icon_value=0)
    split_52809 = col_91F56.split(factor=0.8999999761581421, align=False)
    split_52809.alert = False
    split_52809.enabled = True
    split_52809.active = True
    split_52809.use_property_split = False
    split_52809.use_property_decorate = False
    split_52809.scale_x = 1.0
    split_52809.scale_y = 1.0
    split_52809.alignment = 'Expand'.upper()
    if not True: split_52809.operator_context = "EXEC_DEFAULT"
    split_D3159 = split_52809.split(factor=0.10000000149011612, align=True)
    split_D3159.alert = False
    split_D3159.enabled = True
    split_D3159.active = True
    split_D3159.use_property_split = False
    split_D3159.use_property_decorate = False
    split_D3159.scale_x = 1.0
    split_D3159.scale_y = 1.0
    split_D3159.alignment = 'Expand'.upper()
    if not True: split_D3159.operator_context = "EXEC_DEFAULT"
    split_D3159.prop(bpy.context.scene.sna_rig_tuning_menu, 'show_pivot_points', text='', icon_value=(254 if bpy.context.scene.sna_rig_tuning_menu.show_pivot_points else 253), emboss=True, toggle=True, index=0)
    split_D3159.prop(prop, 'wheels_pivot_points', text='Pivot Point', icon_value=0, emboss=True, index=0)
    op = split_52809.operator('sna.reset_pivot_points_8f3e7', text='', icon_value=715, emboss=True, depress=False)
    split_61BB7 = col_91F56.split(factor=0.8999999761581421, align=False)
    split_61BB7.alert = False
    split_61BB7.enabled = True
    split_61BB7.active = True
    split_61BB7.use_property_split = False
    split_61BB7.use_property_decorate = False
    split_61BB7.scale_x = 1.0
    split_61BB7.scale_y = 1.0
    split_61BB7.alignment = 'Expand'.upper()
    if not True: split_61BB7.operator_context = "EXEC_DEFAULT"
    split_61BB7.prop(prop, 'wheels_turn_radius', text='Turn Radius', icon_value=0, emboss=True, index=0)
    op = split_61BB7.operator('sna.reset_turn_radius_b505e', text='', icon_value=715, emboss=True, depress=False)
    split_385F6 = layout_function.split(factor=0.8999999761581421, align=False)
    split_385F6.alert = False
    split_385F6.enabled = True
    split_385F6.active = True
    split_385F6.use_property_split = False
    split_385F6.use_property_decorate = False
    split_385F6.scale_x = 1.0
    split_385F6.scale_y = 1.0
    split_385F6.alignment = 'Expand'.upper()
    if not True: split_385F6.operator_context = "EXEC_DEFAULT"
    split_385F6.prop(prop, 'wheels_camber_angle', text='Camber Angle', icon_value=0, emboss=True, index=0)
    op = split_385F6.operator('sna.reset_caster_angle_bbefb', text='', icon_value=715, emboss=True, depress=False)


def sna_roll_constraints_3247F(layout_function, ):
    col_2DAD8 = layout_function.column(heading='', align=True)
    col_2DAD8.alert = False
    col_2DAD8.enabled = True
    col_2DAD8.active = True
    col_2DAD8.use_property_split = False
    col_2DAD8.use_property_decorate = False
    col_2DAD8.scale_x = 1.0
    col_2DAD8.scale_y = 1.0
    col_2DAD8.alignment = 'Expand'.upper()
    col_2DAD8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
    col_2DAD8.prop(sna_active_body_C6F79(), 'physics_roll_constraint_button', text='Roll Constraint', icon_value=0, emboss=True, expand=False, toggle=True)
    if sna_active_body_C6F79().physics_roll_constraint_button:
        split_BEAC4 = col_2DAD8.split(factor=0.5, align=True)
        split_BEAC4.alert = False
        split_BEAC4.enabled = True
        split_BEAC4.active = True
        split_BEAC4.use_property_split = False
        split_BEAC4.use_property_decorate = False
        split_BEAC4.scale_x = 1.0
        split_BEAC4.scale_y = 1.0
        split_BEAC4.alignment = 'Expand'.upper()
        if not True: split_BEAC4.operator_context = "EXEC_DEFAULT"
        col_D74F3 = split_BEAC4.column(heading='', align=True)
        col_D74F3.alert = False
        col_D74F3.enabled = True
        col_D74F3.active = True
        col_D74F3.use_property_split = False
        col_D74F3.use_property_decorate = False
        col_D74F3.scale_x = 1.0
        col_D74F3.scale_y = 1.0
        col_D74F3.alignment = 'Expand'.upper()
        col_D74F3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_D74F3.prop(sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint, 'use_limit_ang_x', text='X Axis', icon_value=0, emboss=True, expand=False, toggle=True)
        col_214DE = col_D74F3.column(heading='', align=True)
        col_214DE.alert = False
        col_214DE.enabled = True
        col_214DE.active = sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint.use_limit_ang_x
        col_214DE.use_property_split = False
        col_214DE.use_property_decorate = False
        col_214DE.scale_x = 1.0
        col_214DE.scale_y = 1.0
        col_214DE.alignment = 'Expand'.upper()
        col_214DE.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_214DE.prop(sna_active_body_C6F79(), 'physics_roll_constraint_x_angle', text='Angle', icon_value=0, emboss=True, expand=False, toggle=False)
        col_214DE.prop(sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint, 'spring_stiffness_ang_x', text='Stiffness', icon_value=0, emboss=True, expand=False, toggle=True)
        col_214DE.prop(sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint, 'spring_damping_ang_x', text='Damping', icon_value=0, emboss=True, expand=False, toggle=True)
        col_2FA5F = split_BEAC4.column(heading='', align=True)
        col_2FA5F.alert = False
        col_2FA5F.enabled = True
        col_2FA5F.active = True
        col_2FA5F.use_property_split = False
        col_2FA5F.use_property_decorate = False
        col_2FA5F.scale_x = 1.0
        col_2FA5F.scale_y = 1.0
        col_2FA5F.alignment = 'Expand'.upper()
        col_2FA5F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_2FA5F.prop(sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint, 'use_limit_ang_y', text='Y Axis', icon_value=0, emboss=True, expand=False, toggle=True)
        col_892E7 = col_2FA5F.column(heading='', align=True)
        col_892E7.alert = False
        col_892E7.enabled = True
        col_892E7.active = sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint.use_limit_ang_y
        col_892E7.use_property_split = False
        col_892E7.use_property_decorate = False
        col_892E7.scale_x = 1.0
        col_892E7.scale_y = 1.0
        col_892E7.alignment = 'Expand'.upper()
        col_892E7.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_892E7.prop(sna_active_body_C6F79(), 'physics_roll_constraint_y_angle', text='Angle', icon_value=0, emboss=True, expand=False, toggle=False)
        col_892E7.prop(sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint, 'spring_stiffness_ang_y', text='Stiffness', icon_value=0, emboss=True, expand=False, toggle=True)
        col_892E7.prop(sna_active_body_C6F79().physics_roll_constraint.rigid_body_constraint, 'spring_damping_ang_y', text='Damping', icon_value=0, emboss=True, expand=False, toggle=True)
    if (sna_active_body_C6F79().physics_lean_constraint != None):
        col_93CB4 = layout_function.column(heading='', align=True)
        col_93CB4.alert = False
        col_93CB4.enabled = True
        col_93CB4.active = True
        col_93CB4.use_property_split = False
        col_93CB4.use_property_decorate = False
        col_93CB4.scale_x = 1.0
        col_93CB4.scale_y = 1.0
        col_93CB4.alignment = 'Expand'.upper()
        col_93CB4.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_93CB4.prop(sna_active_body_C6F79().physics_lean_constraint.rigid_body_constraint, 'enabled', text='Lean Constraint', icon_value=0, emboss=True, expand=False, toggle=True)
        if sna_active_body_C6F79().physics_lean_constraint.rigid_body_constraint.enabled:
            col_93CB4.prop(sna_active_body_C6F79(), 'physics_lean_strength', text='Lean Strength', icon_value=0, emboss=True, expand=False, toggle=False)


def sna_auto_steering_B7156(angle_diff, length, Distance, Prop, Reverse_Angle, Auto_Reverse):
    if Auto_Reverse:
        if (((angle_diff > Reverse_Angle) and (angle_diff < 180.0)) or ((angle_diff < float(Reverse_Angle * -1.0)) and (angle_diff > -180.0))):
            Prop.rig_drivers.steering = float(float(angle_diff / 35.0) * -1.0)
        else:
            Prop.rig_drivers.steering = float(angle_diff / 35.0)
    else:
        Prop.rig_drivers.steering = float(angle_diff / 35.0)
    return (Auto_Reverse and (((angle_diff > Reverse_Angle) and (angle_diff < 180.0)) or ((angle_diff < float(Reverse_Angle * -1.0)) and (angle_diff > -180.0))))


def sna_auto_brake_52573(Length, Distance, Prop, Input):
    if ((Length < Distance) and Input):
        Prop.rig_drivers.brake = True
    else:
        Prop.rig_drivers.brake = False


@persistent
def frame_change_pre_handler_87138(dummy):
    pass


def sna_brake_func_EE862(Motor_Constraint, Brake_Strength):
    Motor_Constraint.rigid_body_constraint.motor_ang_target_velocity = 0.0
    Motor_Constraint.rigid_body_constraint.motor_ang_max_impulse = Brake_Strength


def sna_set_frame_0C83A(Brake, Input, Deceleration):
    if ((bpy.context.scene.frame_current == bpy.context.scene.frame_start) or Brake):
        Input.first_frame = bpy.context.scene.frame_current
    return Input.first_frame


def sna_framerange_70DBF(Brake, TIme, Prop, Input):
    output_0_6357c = sna_set_frame_0C83A((Brake or (Prop.target_speed == 0.0)), Prop, (Prop.target_speed == 0.0))
    if ((bpy.context.scene.frame_current == bpy.context.scene.frame_start) or Brake):
        Prop.acceleration = 1.0
    if (Prop.target_speed == 0.0):
        Prop.acceleration = float(max(0.0, min(float(Prop.acceleration - 0.5), Prop.acceleration)))
    else:
        if (Prop.acceleration < float(TIme * bpy.context.scene.render.fps)):
            Prop.acceleration = float(max(0.0, min(float(Prop.acceleration + 1.0), float(TIme * bpy.context.scene.render.fps))))
    return float(max(0.0, min(Prop.acceleration, float(TIme * bpy.context.scene.render.fps))))


def sna_axle_steering_6B437(Axle_Prop, Steering, Steering_Power):
    for i_C0EA3 in range(len(Axle_Prop.axle_wheels)):
        if Axle_Prop.axle_wheels[i_C0EA3].wheel_steeringmotor.rigid_body_constraint.enabled:
            sna_steering_func_49371(Steering, Axle_Prop.axle_wheels[i_C0EA3].wheel_steeringmotor, Axle_Prop.axle_wheels[i_C0EA3].wheel_constraint, Axle_Prop.rig_tuning_group.wheels_turn_radius, float(Steering_Power * 2.0), Axle_Prop.axle_wheels[i_C0EA3].wheel_rb)


def sna_steering_func_49371(Value, Steering_Constraint, Wheel_Constraint, Turn_Radius, Steering_Power, Wheel_RB):
    Wheel_Constraint.rigid_body_constraint.spring_stiffness_ang_z = float(eval("Wheel_RB.dimensions[0] + Wheel_RB.dimensions[1] + Wheel_RB.dimensions[2] / 3") * float(bpy.context.scene.rigidbody_world.substeps_per_frame * 15.0) * Wheel_RB.rigid_body.mass)
    Wheel_Constraint.rigid_body_constraint.spring_damping_ang_z = float(float(eval("Wheel_RB.dimensions[0] + Wheel_RB.dimensions[1] + Wheel_RB.dimensions[2] / 3") * float(bpy.context.scene.rigidbody_world.substeps_per_frame * 15.0) * Wheel_RB.rigid_body.mass) / float(Steering_Power / 1.0))
    Steering_Constraint.rigid_body_constraint.motor_ang_target_velocity = (0.0 if (Value == 0.0) else float((float(Steering_Power * -1.0) if (Value < 0.0) else Steering_Power) / 10.0))
    if (Value == 0.0):
        output_0_3c9f6, output_001_1_3c9f6 = sna_steering_lock_FD05B()
        if output_0_3c9f6:
            Wheel_Constraint.rigid_body_constraint.spring_stiffness_ang_z = 1000000.0
            Wheel_Constraint.rigid_body_constraint.spring_damping_ang_z = 1000000.0
        else:
            Wheel_Constraint.rigid_body_constraint.spring_stiffness_ang_z = float(float(eval("Wheel_RB.dimensions[0] + Wheel_RB.dimensions[1] + Wheel_RB.dimensions[2] / 3") * float(bpy.context.scene.rigidbody_world.substeps_per_frame * 15.0) * Wheel_RB.rigid_body.mass) / 3.0)
            Wheel_Constraint.rigid_body_constraint.spring_damping_ang_z = float(float(eval("Wheel_RB.dimensions[0] + Wheel_RB.dimensions[1] + Wheel_RB.dimensions[2] / 3") * float(bpy.context.scene.rigidbody_world.substeps_per_frame * 15.0) * Wheel_RB.rigid_body.mass) / float(Steering_Power / 1.0))
            Steering_Constraint.rigid_body_constraint.motor_ang_max_impulse = 0.0
    else:
        Steering_Constraint.rigid_body_constraint.motor_ang_max_impulse = float(eval("Wheel_RB.dimensions[0] + Wheel_RB.dimensions[1] + Wheel_RB.dimensions[2] / 3") * float(Turn_Radius * (float(Value * -1.0) if (Value < 0.0) else Value) * float(bpy.context.scene.rigidbody_world.substeps_per_frame * 15.0)) * Wheel_RB.rigid_body.mass)


def sna_accelerator2_86EA1(Value, Max, Time, speed, Input, Torque, Acceleration, Prop):
    if (Max == 0.0):
        pass
    else:
        Prop.current_speed = Max
    return float(max(0.0, min(eval("(float((Prop.current_speed if (Max == 0.0) else Max) * -1.0) if ((Prop.current_speed if (Max == 0.0) else Max) < 0.0) else (Prop.current_speed if (Max == 0.0) else Max)) * (1 - ((1 - (Acceleration/(float(Time * 1.0)*bpy.context.scene.render.fps))) ** 3))"), (float((Prop.current_speed if (Max == 0.0) else Max) * -1.0) if ((Prop.current_speed if (Max == 0.0) else Max) < 0.0) else (Prop.current_speed if (Max == 0.0) else Max)))))


def sna_differential_steering_175CE(Axle_Prop, Drive, Torque, Steering, Wheel_Weight, Wheel_DIM, Target_Speed, Wheel_Radius):
    if (Steering < 0.0):
        sna_drive_func_646F1(Axle_Prop.axle_wheels[0].wheel_motor, Drive, Torque, Wheel_Weight, Wheel_DIM, 0.0, Target_Speed, Wheel_Radius)
        sna_drive_func_646F1(Axle_Prop.axle_wheels[1].wheel_motor, float(Drive * (float(Steering * -1.0) if (Steering < 0.0) else Steering)), Torque, Wheel_Weight, Wheel_DIM, 0.0, float(Target_Speed * -1.0), Wheel_Radius)
    if (Steering > 0.0):
        sna_drive_func_646F1(Axle_Prop.axle_wheels[0].wheel_motor, float(Drive * (float(Steering * -1.0) if (Steering < 0.0) else Steering)), Torque, Wheel_Weight, Wheel_DIM, 0.0, float(Target_Speed * -1.0), Wheel_Radius)
        sna_drive_func_646F1(Axle_Prop.axle_wheels[1].wheel_motor, Drive, Torque, Wheel_Weight, Wheel_DIM, 0.0, Target_Speed, Wheel_Radius)
    if (Steering == 0.0):
        sna_drive_func_646F1(Axle_Prop.axle_wheels[0].wheel_motor, Drive, Torque, Wheel_Weight, Wheel_DIM, 0.0, Target_Speed, Wheel_Radius)
        sna_drive_func_646F1(Axle_Prop.axle_wheels[1].wheel_motor, Drive, Torque, Wheel_Weight, Wheel_DIM, 0.0, Target_Speed, Wheel_Radius)


@persistent
def frame_change_pre_handler_B5700(dummy):
    if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()):
        for i_C4652 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            for i_9D04F in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_C4652])[0])):
                if bpy.context.scene.sna_rbc_rig_collection[i_C4652].rig_drivers.brake:
                    sna_brake_func_EE862(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_C4652])[0][i_9D04F].wheel_motor, float(float(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_C4652])[0][i_9D04F].wheel_rb.rigid_body.mass * bpy.context.scene.sna_rbc_rig_collection[i_C4652].rig_drivers.brake_strength) * 2.0))


@persistent
def frame_change_pre_handler_EE4B7(dummy):
    if (property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()) and bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged):
        for i_F37BC in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            if (bpy.context.scene.sna_rbc_rig_collection[i_F37BC].rig_bodies[0].body_model != None):
                for i_4DBC6 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_F37BC])[2])):
                    if (i_4DBC6 == 0):
                        sna_axle_steering_6B437(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_F37BC])[2][i_4DBC6], bpy.context.scene.sna_rbc_rig_collection[i_F37BC].rig_drivers.steering, bpy.context.scene.sna_rbc_rig_collection[i_F37BC].rig_drivers.steering_power)
                    else:
                        sna_axle_steering_6B437(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_F37BC])[2][i_4DBC6], float(bpy.context.scene.sna_rbc_rig_collection[i_F37BC].rig_drivers.steering * -1.0), bpy.context.scene.sna_rbc_rig_collection[i_F37BC].rig_drivers.steering_power)


def sna_steering_lock_FD05B():
    for i_04ACD in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
        for i_ED8C6 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_04ACD].body_rb.sna_body_axles)):
            if 'Steering' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_04ACD].body_rb.sna_body_axles[i_ED8C6].axle_type:
                return [(round(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_04ACD].body_model.matrix_world.to_euler()[2], abs(3)) == round(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_04ACD].body_rb.sna_body_axles[i_ED8C6].axle_wheels[0].wheel_model.matrix_world.to_euler()[2], abs(3))), math.degrees(float(round(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_04ACD].body_model.matrix_world.to_euler()[2], abs(3)) - round(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_04ACD].body_rb.sna_body_axles[i_ED8C6].axle_wheels[0].wheel_model.matrix_world.to_euler()[2], abs(3))))]


@persistent
def frame_change_pre_handler_A3B96(dummy):
    if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()):
        for i_DED52 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            if ((bpy.context.scene.frame_current == bpy.context.scene.frame_start) or bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.brake):
                bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.drive = 0.0
            else:
                if (bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.time == 0.0):
                    bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.drive = (float(bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.target_speed * -1.0) if (bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.target_speed < 0.0) else bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.target_speed)
                else:
                    value_0_bc299 = sna_accelerator2_86EA1(bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.drive, bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.target_speed, bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.time, 0.0, (bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.target_speed == 0.0), bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.torque, bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.acceleration, bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers)
                    bpy.context.scene.sna_rbc_rig_collection[i_DED52].rig_drivers.drive = value_0_bc299


def sna_drive_func_646F1(Motor_Constraint, Drive, Motor_Torque, Wheel_Weight, Wheel_DIM, Time, Target_Speed, Wheel_Radius):
    Motor_Constraint.rigid_body_constraint.motor_ang_target_velocity = float(eval("((float((float(Drive * -1.0) if (Target_Speed < 0.0) else Drive) * 0.625) if (bpy.context.scene.sna_speed_unit == 'Km/h') else (float(Drive * -1.0) if (Target_Speed < 0.0) else Drive)) * 0.44704) / Wheel_Radius") * -1.0)
    Motor_Constraint.rigid_body_constraint.motor_ang_max_impulse = float(Wheel_DIM * Drive * Wheel_Weight * float(Motor_Torque / 1.0))
    if (Target_Speed == 0.0):
        Motor_Constraint.rigid_body_constraint.motor_ang_max_impulse = float(Wheel_Weight * 2.0)


@persistent
def frame_change_pre_handler_C5D97(dummy):
    if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()):
        for i_200F7 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            sna_framerange_70DBF(bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.brake, bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.time, bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers, None)
            if bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.brake:
                pass
            else:
                for i_7D28F in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2])):
                    for i_6B948 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels)):
                        if sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_motor.rigid_body_constraint.enabled:
                            if 'Differential Steering' in sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_type:
                                sna_differential_steering_175CE(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F], bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.drive, bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.torque, bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.steering, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.rigid_body.mass, eval("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[0] + sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[1] + sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[2] / 3"), bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.target_speed, float(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[0] / 2.0))
                            else:
                                sna_drive_func_646F1(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_motor, bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.drive, float(bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.torque / 2.0), sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.rigid_body.mass, eval("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[0] + sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[1] + sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[2] / 3"), bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.time, bpy.context.scene.sna_rbc_rig_collection[i_200F7].rig_drivers.target_speed, float(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[i_200F7])[2][i_7D28F].axle_wheels[i_6B948].wheel_rb.dimensions[0] / 2.0))


@persistent
def frame_change_pre_handler_9218D(dummy):
    if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()):
        for i_206B2 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            if bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.enable_guide:
                if (bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.guide_object != None):
                    obj1 = bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.guide_object
                    obj2 = bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_bodies[0].body_rb
                    angle = None
                    angle_diff = None
                    polar_angle = None
                    length = None
                    import math
                    # Get the position vectors of the two objects
                    pos1 = obj1.matrix_world.to_translation()
                    pos2 = obj2.matrix_world.to_translation()
                    # Get the rotation of obj2 as Euler angles
                    rot1 = obj2.matrix_world.to_euler()
                    # Calculate the difference between the position vectors
                    diff = pos2 - pos1
                    length = math.sqrt(diff.x**2 + diff.y**2)
                    # Calculate the polar angle between the objects
                    polar_angle = math.atan2(diff.x, diff.y)
                    # Convert the angle to degrees (optional)
                    polar_angle = math.degrees(polar_angle)
                    # Convert the rotation of obj2 to degrees
                    angle = math.degrees(rot1.z)
                    # Find the difference between the polar angle and the rotation of obj2
                    angle_diff = polar_angle + angle
                    # Make sure the result is between -180 and 180 degrees
                    angle_diff = (angle_diff + 180) % 360 - 180
                    # Take the absolute value of the polar angle and the angle
                    polar_angleabs = abs(polar_angle)
                    angleabs = abs(angle)
                    bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.length = length
                    if bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.auto_brake:
                        sna_auto_brake_52573(length, bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.distance, bpy.context.scene.sna_rbc_rig_collection[i_206B2], bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.auto_brake)
                    output_0_ad5ff = sna_auto_steering_B7156(angle_diff, 0.0, 0.0, bpy.context.scene.sna_rbc_rig_collection[i_206B2], math.degrees(bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.reverse_angle), bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.auto_reverse)
                    sna_auto_drive_1992B(length, bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.distance, bpy.context.scene.sna_rbc_rig_collection[i_206B2], angle_diff, bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_drivers.target_speed, output_0_ad5ff, math.degrees(bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.reverse_angle), bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.auto_drive)
                if (bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.guide_path != None):
                    obj = bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_bodies[0].body_rb.sna_body_axles[0].axle_wheels[0].wheel_rb
                    curve = bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.guide_path
                    guide_obj = bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.guide_object
                    path_distance = bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_guide_control.guide_path_distance
                    car_body = bpy.context.scene.sna_rbc_rig_collection[i_206B2].rig_bodies[0].body_rb
                    nearest = None
                    distance = None
                    matrix = None
                    BigD = None
                    from mathutils import Vector

                    def nearest_points_on_curve(curve, matrix, max_distance=path_distance, min_distance=0 ):
                        points = []
                        points_i = []
                        num_samples = curve.data.resolution_u *2
                        for spline in curve.data.splines:
                            if spline.type == 'BEZIER':
                                for i in range(len(spline.bezier_points) - 1):
                                    bezier = spline.bezier_points[i:i+2]
                                    for j in range(num_samples):
                                        t = j / (num_samples - 1)
                                        curve_point = (1-t)**3 * bezier[0].co + 3*(1-t)**2*t*bezier[0].handle_right + 3*(1-t)*t**2*bezier[1].handle_left + t**3 * bezier[1].co
                                        curve_point = curve.matrix_world @ curve_point
                                        curve_point = Vector(curve_point[:3])
                                        distance = (matrix.translation.xy - Vector((curve_point.x, curve_point.y))).length
                                        if distance <= max_distance and distance >= min_distance :
                                            point_i = (curve_point, i)
                                            points_i.append(point_i)
                                            if not points_i or i <= points_i[0][1] + 1 and i>= points_i[-1][1] - 1:
                                                points.append(curve_point)
                        return points

                    def set_guide_location(guide_obj, nearest_points, matrix, current_point_index, max_distance=path_distance):
                        if current_point_index >= len(nearest_points):
                            return
                        next_point_index = current_point_index + 1
                        if next_point_index >= len(nearest_points):
                            return
                        current_point = nearest_points[current_point_index]
                        next_point = nearest_points[next_point_index]
                        current_distance = (matrix.translation.xy - Vector((current_point.x, current_point.y))).length
                        next_distance = (matrix.translation.xy - Vector((next_point.x, next_point.y))).length
                        if current_distance <= max_distance and next_distance <= max_distance:
                            guide_obj.location = current_point
                            tangent = (next_point - current_point).normalized()
                            guide_obj.rotation_mode = 'QUATERNION'
                            guide_obj.rotation_quaternion = tangent.to_track_quat('Z', 'Y')
                        return next_point_index
                    # Example usage
                    if obj and guide_obj and curve:
                        matrix = obj.matrix_world
                        nearest_points = nearest_points_on_curve(curve, matrix)
                        current_point_index = 0
                        while True:
                            current_point_index = set_guide_location(guide_obj, nearest_points, matrix, current_point_index)
                            if current_point_index is None:
                                break


def sna_auto_drive_1992B(Length, Distance, Prop, angle_diff, Top_Speed, Auto_Reverse, Reverse_angle, Auto_Drive):
    if Auto_Reverse:
        Prop.rig_drivers.target_speed = (float(float(max(Prop.rig_guide_control.min_speed, min(float(Length * 1.0), Prop.rig_guide_control.max_speed))) * -1.0) if Auto_Drive else (float(Top_Speed * -1.0) if (Top_Speed > 0.0) else Top_Speed))
    else:
        Prop.rig_drivers.target_speed = (float(max(Prop.rig_guide_control.min_speed, min(float(Length * 1.0), Prop.rig_guide_control.max_speed))) if Auto_Drive else (float(Top_Speed * -1.0) if (Top_Speed < 0.0) else Top_Speed))


@persistent
def frame_change_pre_handler_EE3CA(dummy):
    if (property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig]", globals(), locals()) and bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged):
        for i_2C846 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            if 'Motorcycle' in bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_type:
                if bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_bodies[0].physics_lean_constraint.rigid_body_constraint.enabled:
                    bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_bodies[0].physics_lean_constraint.rigid_body_constraint.motor_ang_target_velocity = bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_drivers.steering
                    bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_bodies[0].physics_lean_constraint.rigid_body_constraint.motor_ang_max_impulse = float((float(bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_drivers.steering * -1.0) if (bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_drivers.steering < 0.0) else bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_drivers.steering) * bpy.context.scene.sna_rbc_rig_collection[i_2C846].rig_bodies[0].physics_lean_strength)


class SNA_PT_RBC_RIG_0A7A5(bpy.types.Panel):
    bl_label = 'RBC Rig'
    bl_idname = 'SNA_PT_RBC_RIG_0A7A5'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'RBC'
    bl_order = 3
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not ((not (property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0)))

    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=37, scale=1.0)

    def draw(self, context):
        layout = self.layout
        col_68E43 = layout.column(heading='', align=False)
        col_68E43.alert = False
        col_68E43.enabled = True
        col_68E43.active = True
        col_68E43.use_property_split = False
        col_68E43.use_property_decorate = False
        col_68E43.scale_x = 1.0
        col_68E43.scale_y = 1.0
        col_68E43.alignment = 'Expand'.upper()
        col_68E43.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_BE2F1 = col_68E43.column(heading='', align=True)
        col_BE2F1.alert = False
        col_BE2F1.enabled = True
        col_BE2F1.active = True
        col_BE2F1.use_property_split = False
        col_BE2F1.use_property_decorate = False
        col_BE2F1.scale_x = 1.0
        col_BE2F1.scale_y = 1.25
        col_BE2F1.alignment = 'Expand'.upper()
        col_BE2F1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_BE2F1.prop(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig], 'rig_name', text='', icon_value=0, emboss=True, index=1)
        row_55C1D = col_BE2F1.row(heading='', align=True)
        row_55C1D.alert = False
        row_55C1D.enabled = True
        row_55C1D.active = True
        row_55C1D.use_property_split = False
        row_55C1D.use_property_decorate = False
        row_55C1D.scale_x = 1.0
        row_55C1D.scale_y = 1.0
        row_55C1D.alignment = 'Expand'.upper()
        row_55C1D.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_55C1D.prop(bpy.context.scene, 'sna_rbc_rig_panel', text=' ', icon_value=0, emboss=True, expand=True)
        col_82537 = col_68E43.column(heading='', align=True)
        col_82537.alert = False
        col_82537.enabled = True
        col_82537.active = True
        col_82537.use_property_split = False
        col_82537.use_property_decorate = False
        col_82537.scale_x = 1.0
        col_82537.scale_y = 1.0
        col_82537.alignment = 'Expand'.upper()
        col_82537.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_9DDFF = col_82537.column(heading='', align=True)
        col_9DDFF.alert = False
        col_9DDFF.enabled = True
        col_9DDFF.active = True
        col_9DDFF.use_property_split = False
        col_9DDFF.use_property_decorate = False
        col_9DDFF.scale_x = 1.0
        col_9DDFF.scale_y = 0.5
        col_9DDFF.alignment = 'Expand'.upper()
        col_9DDFF.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_9DDFF.label(text='', icon_value=0)
        for i_6FC48 in range(len(list(bpy.context.scene.sna_rbc_rig_panel))):
            if list(bpy.context.scene.sna_rbc_rig_panel)[i_6FC48] == "Tuning":
                layout_function = col_82537
                sna_tuning_panel_F3327(layout_function, )
            elif list(bpy.context.scene.sna_rbc_rig_panel)[i_6FC48] == "Controls":
                layout_function = col_82537
                sna_controls_panel_284BB(layout_function, )
            elif list(bpy.context.scene.sna_rbc_rig_panel)[i_6FC48] == "Set Up":
                layout_function = col_82537
                sna_set_up_panel_DACC3(layout_function, )
            else:
                pass


def sna_rbc_rig_panel_icon_enum_items(self, context):
    enum_items = ['CONSTRAINT', 'MODIFIER', 'OPTIONS']
    return [make_enum_item(item[0], item[1], item[2], item[3], i) for i, item in enumerate(enum_items)]


def sna_rbc_rig_panel_enum_items(self, context):
    enum_items = [['Set Up', 'Set Up', '', 175], ['Tuning', 'Tuning', '', 94], ['Controls', 'Controls', '', 23]]
    return [make_enum_item(item[0], item[1], item[2], item[3], 2**i) for i, item in enumerate(enum_items)]


def sna_fancy_rig_control_panel_BC7FE(layout_function, ):
    if 'Controls' in str(list(bpy.context.scene.sna_rbc_rig_panel)):
        row_B8F46 = layout_function.row(heading='', align=True)
        row_B8F46.alert = False
        row_B8F46.enabled = True
        row_B8F46.active = True
        row_B8F46.use_property_split = False
        row_B8F46.use_property_decorate = False
        row_B8F46.scale_x = 2.0
        row_B8F46.scale_y = 1.2000000476837158
        row_B8F46.alignment = 'Expand'.upper()
        row_B8F46.operator_context = "INVOKE_DEFAULT" if False else "EXEC_DEFAULT"
        col_11C17 = row_B8F46.column(heading='', align=True)
        col_11C17.alert = False
        col_11C17.enabled = True
        col_11C17.active = True
        col_11C17.use_property_split = False
        col_11C17.use_property_decorate = False
        col_11C17.scale_x = 1.0
        col_11C17.scale_y = 1.0
        col_11C17.alignment = 'Expand'.upper()
        col_11C17.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_11C17.prop_enum(bpy.context.scene, 'sna_rig_control_panel', text=('      Drivers' if (bpy.context.scene.sna_rig_control_panel == 'Drivers') else ''), value='Drivers')
        col_2F2D3 = col_11C17.column(heading='', align=True)
        col_2F2D3.alert = False
        col_2F2D3.enabled = True
        col_2F2D3.active = True
        col_2F2D3.use_property_split = False
        col_2F2D3.use_property_decorate = False
        col_2F2D3.scale_x = 1.0
        col_2F2D3.scale_y = -1.0
        col_2F2D3.alignment = 'Expand'.upper()
        col_2F2D3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_2F2D3.template_icon(icon_value=0, scale=1.0)
        row_CFAE1 = col_11C17.row(heading='', align=False)
        row_CFAE1.alert = False
        row_CFAE1.enabled = True
        row_CFAE1.active = True
        row_CFAE1.use_property_split = False
        row_CFAE1.use_property_decorate = True
        row_CFAE1.scale_x = 1.0
        row_CFAE1.scale_y = 1.0
        row_CFAE1.alignment = 'Expand'.upper()
        row_CFAE1.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_CFAE1.template_icon(icon_value=486, scale=1.0)
        if (bpy.context.scene.sna_rig_control_panel == 'Drivers'):
            row_CFAE1.label(text='', icon_value=0)
        col_F07B3 = row_B8F46.column(heading='', align=True)
        col_F07B3.alert = False
        col_F07B3.enabled = True
        col_F07B3.active = True
        col_F07B3.use_property_split = False
        col_F07B3.use_property_decorate = False
        col_F07B3.scale_x = 1.0
        col_F07B3.scale_y = 1.0
        col_F07B3.alignment = 'Expand'.upper()
        col_F07B3.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_F07B3.prop_enum(bpy.context.scene, 'sna_rig_control_panel', text=('          Controller' if (bpy.context.scene.sna_rig_control_panel == 'Controller') else ''), value='Controller')
        col_6788B = col_F07B3.column(heading='', align=True)
        col_6788B.alert = False
        col_6788B.enabled = True
        col_6788B.active = True
        col_6788B.use_property_split = False
        col_6788B.use_property_decorate = False
        col_6788B.scale_x = 1.0
        col_6788B.scale_y = -1.0
        col_6788B.alignment = 'Expand'.upper()
        col_6788B.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_6788B.template_icon(icon_value=0, scale=1.0)
        row_67EBC = col_F07B3.row(heading='', align=False)
        row_67EBC.alert = False
        row_67EBC.enabled = True
        row_67EBC.active = True
        row_67EBC.use_property_split = False
        row_67EBC.use_property_decorate = False
        row_67EBC.scale_x = 1.0
        row_67EBC.scale_y = 1.0
        row_67EBC.alignment = 'Expand'.upper()
        row_67EBC.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_67EBC.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Controller_Icon.png')), scale=1.0)
        if (bpy.context.scene.sna_rig_control_panel == 'Controller'):
            row_67EBC.label(text='', icon_value=0)
        col_4EB16 = row_B8F46.column(heading='', align=True)
        col_4EB16.alert = False
        col_4EB16.enabled = True
        col_4EB16.active = True
        col_4EB16.use_property_split = False
        col_4EB16.use_property_decorate = False
        col_4EB16.scale_x = 1.0
        col_4EB16.scale_y = 1.0
        col_4EB16.alignment = 'Expand'.upper()
        col_4EB16.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_4EB16.prop_enum(bpy.context.scene, 'sna_rig_control_panel', text=('         Keyboard' if (bpy.context.scene.sna_rig_control_panel == 'Keyboard') else ''), value='Keyboard')
        col_39CE2 = col_4EB16.column(heading='', align=True)
        col_39CE2.alert = False
        col_39CE2.enabled = True
        col_39CE2.active = True
        col_39CE2.use_property_split = False
        col_39CE2.use_property_decorate = False
        col_39CE2.scale_x = 1.0
        col_39CE2.scale_y = -1.0
        col_39CE2.alignment = 'Expand'.upper()
        col_39CE2.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_39CE2.template_icon(icon_value=0, scale=1.0)
        row_F85C8 = col_4EB16.row(heading='', align=False)
        row_F85C8.alert = False
        row_F85C8.enabled = True
        row_F85C8.active = True
        row_F85C8.use_property_split = False
        row_F85C8.use_property_decorate = False
        row_F85C8.scale_x = 1.0
        row_F85C8.scale_y = 1.0
        row_F85C8.alignment = 'Expand'.upper()
        row_F85C8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_F85C8.template_icon(icon_value=load_preview_icon(os.path.join(os.path.dirname(__file__), 'assets', 'RBC_Keyboard_Icon.png')), scale=1.0)
        if (bpy.context.scene.sna_rig_control_panel == 'Keyboard'):
            row_F85C8.label(text='', icon_value=0)
        col_8A8F9 = row_B8F46.column(heading='', align=True)
        col_8A8F9.alert = False
        col_8A8F9.enabled = True
        col_8A8F9.active = True
        col_8A8F9.use_property_split = False
        col_8A8F9.use_property_decorate = False
        col_8A8F9.scale_x = 1.0
        col_8A8F9.scale_y = 1.0
        col_8A8F9.alignment = 'Expand'.upper()
        col_8A8F9.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_8A8F9.prop_enum(bpy.context.scene, 'sna_rig_control_panel', text=('     Guides' if (bpy.context.scene.sna_rig_control_panel == 'Guides') else ''), value='Guides')
        col_618F8 = col_8A8F9.column(heading='', align=True)
        col_618F8.alert = False
        col_618F8.enabled = True
        col_618F8.active = True
        col_618F8.use_property_split = False
        col_618F8.use_property_decorate = False
        col_618F8.scale_x = 1.0
        col_618F8.scale_y = -1.0
        col_618F8.alignment = 'Expand'.upper()
        col_618F8.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_618F8.template_icon(icon_value=0, scale=1.0)
        row_EC59A = col_8A8F9.row(heading='', align=False)
        row_EC59A.alert = False
        row_EC59A.enabled = True
        row_EC59A.active = True
        row_EC59A.use_property_split = False
        row_EC59A.use_property_decorate = True
        row_EC59A.scale_x = 1.0
        row_EC59A.scale_y = 1.0
        row_EC59A.alignment = 'Expand'.upper()
        row_EC59A.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        row_EC59A.template_icon(icon_value=146, scale=1.0)
        if (bpy.context.scene.sna_rig_control_panel == 'Guides'):
            row_EC59A.label(text='', icon_value=0)


def sna_add_rbc_scene_DCE04():
    if (bpy.context.scene.sna_rbc_addon_collection == None):
        bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
        collection_1B90E = bpy.data.collections.new(name='RBC Addon', )
        bpy.context.scene.collection.children.link(child=collection_1B90E, )
        collection_1B90E.hide_select = False
        bpy.context.scene.sna_rbc_addon_collection = collection_1B90E
        bpy.ops.sna.add_ground_28971('INVOKE_DEFAULT', )
        sna_add_follow_camera_01217()
        sna_add_chase_camera_A9BFA()
        sna_set_rb_world_21020()
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection


class SNA_OT_Add_Ground_28971(bpy.types.Operator):
    bl_idname = "sna.add_ground_28971"
    bl_label = "Add Ground"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add('INVOKE_DEFAULT', size=150.0, location=(0.0, 0.0, 0.0))
        bpy.context.view_layer.objects.active.name = 'RBC Ground'
        bpy.context.scene.sna_rbc_scene_.ground = bpy.context.view_layer.objects.active
        bpy.ops.rigidbody.object_add('INVOKE_DEFAULT', type='PASSIVE')
        bpy.context.view_layer.objects.active.rigid_body.collision_collections = (True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
        sna_ground_mat_BE385()
        bpy.context.scene.sna_rbc_scene_.ground.data.materials.append(material=bpy.data.materials['RBC Ground'], )
        sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, False, True, True)
        sna_link_obj_B65F4(bpy.context.view_layer.objects.active, bpy.data.collections['RBC Addon'])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_ground_mat_BE385():
    if property_exists("bpy.data.materials['RBC Ground']", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.materials)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'RBC Assets.blend') + r'\Material', filename='RBC Ground', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.materials)))
        appended_F6C23 = None if not new_data else new_data[0]


def sna_add_follow_camera_01217():
    bpy.ops.object.camera_add('INVOKE_DEFAULT', align='WORLD', location=(5.0, 5.0, 5.0))
    bpy.context.view_layer.objects.active.name = 'RBC Follow Camera'
    constraint_375A2 = bpy.context.view_layer.objects.active.constraints.new(type='TRACK_TO', )
    constraint_375A2.name = 'RBC Track To'
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, bpy.data.collections['RBC Addon'])
    bpy.context.scene.sna_rbc_scene_.follow_camera = bpy.context.view_layer.objects.active


@persistent
def frame_change_pre_handler_156BA(dummy):
    if (bpy.context.scene.rigidbody_world.point_cache.frame_end != bpy.context.scene.frame_end):
        bpy.context.scene.rigidbody_world.point_cache.frame_end = bpy.context.scene.frame_end


def sna_set_rb_world_21020():
    bpy.context.scene.rigidbody_world.use_split_impulse = True
    bpy.context.scene.sna_rbc_scene_.performance = 'High'


def sna_add_chase_camera_A9BFA():
    bpy.ops.object.camera_add('INVOKE_DEFAULT', align='WORLD', location=(0.0, 5.0, 5.0))
    bpy.context.view_layer.objects.active.name = 'RBC Chase Camera'
    constraint_48B15 = bpy.context.view_layer.objects.active.constraints.new(type='CHILD_OF', )
    constraint_48B15.name = 'RBC Chase Cam'
    constraint_48B15.use_rotation_x = False
    constraint_48B15.use_rotation_y = False
    constraint_B56A3 = bpy.context.view_layer.objects.active.constraints.new(type='TRACK_TO', )
    constraint_B56A3.name = 'RBC Track To'
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, bpy.data.collections['RBC Addon'])
    bpy.context.scene.sna_rbc_scene_.chase_camera = bpy.context.view_layer.objects.active


def sna_rbc_body_collision_type_ADADE(Input):
    for i_9CEBF in range(len(bpy.context.scene.sna_rbc_rig_collection)):
        for i_B4CD9 in range(len(bpy.context.scene.sna_rbc_rig_collection[i_9CEBF].rig_bodies)):
            bpy.context.scene.sna_rbc_rig_collection[i_9CEBF].rig_bodies[i_B4CD9].body_rb.rigid_body.collision_shape = Input


def sna_set_temp_active_obj_323A4(Temp_Active_Obj, Set_new_Active_Obj):
    if Set_new_Active_Obj:
        rbc_scenecollections['sna_active_obj'] = bpy.context.view_layer.objects.active
        bpy.context.view_layer.objects.active = Temp_Active_Obj
    else:
        bpy.context.view_layer.objects.active = rbc_scenecollections['sna_active_obj']
        rbc_scenecollections['sna_active_obj'] = None


def sna_set_camera_C716A():
    if ((property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies) > 0) and (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_model != None)):
        bpy.context.scene.sna_rbc_scene_.follow_camera.constraints['RBC Track To'].target = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_model
    if ((property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies) > 0) and (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_model != None)):
        bpy.context.scene.sna_rbc_scene_.chase_camera.constraints['RBC Chase Cam'].target = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_model
        bpy.context.scene.sna_rbc_scene_.chase_camera.constraints['RBC Track To'].target = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_model
        bpy.context.scene.sna_rbc_scene_.chase_camera.location = (0.0, float(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_model.location[1] + 10.0), float(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_model.location[2] + 2.0))
        sna_set_temp_active_obj_323A4(bpy.context.scene.sna_rbc_scene_.chase_camera, True)
        bpy.ops.constraint.childof_clear_inverse('INVOKE_DEFAULT', constraint='RBC Chase Cam', owner='OBJECT')
        sna_set_temp_active_obj_323A4(None, False)


def sna_rig_auto_select_55240():
    if (bpy.context.scene.sna_auto_select_rig and property_exists("sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][0]", globals(), locals())):
        bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
        for i_8497F in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_8497F].body_rb.hide_select = False
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_8497F].body_rb.select_set(state=True, )
            blender_version = bpy.app.version
            use_temp_override = blender_version >= (3, 3, 0)
            # Override the poll method of view_selected operator
            if use_temp_override:
                for area in bpy.context.screen.areas:
                    if area.type == "VIEW_3D":
                        override = bpy.context.copy()
                    # change context to the sequencer
                        override["area"] = area
                        override["region"] = area.regions[-1]
                    # run the command with the correct context
                        with bpy.context.temp_override(**override):
                            bpy.ops.view3d.view_selected(use_all_regions=False)
                        break
            else:
                # For Blender version < 3.3.0, override the entire operator
                for area in bpy.context.screen.areas:
                    if area.type == 'VIEW_3D':
                        ctx = bpy.context.copy()
                        ctx['area'] = area
                        ctx['region'] = area.regions[-1]
                        bpy.ops.view3d.view_selected(ctx)
            sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_8497F].body_rb.hide_select = True


def sna_create_rbc_collection_7D211(ID):
    if ((property_exists("bpy.context.scene.sna_rbc_rig_collection", globals(), locals()) and len(bpy.context.scene.sna_rbc_rig_collection) > 0) and (bpy.context.scene.sna_rbc_addon_collection == None)):
        sna_add_rbc_scene_DCE04()
    coll_0_233f9 = sna_add_collection_98332('RBC ' + ID.rig_name + '', True, bpy.context.scene.sna_rbc_addon_collection, True, None)


def sna_add_collection_98332(Coll_Name, Link, Link_Coll, Hide_Render, Input_001):
    rbc_scenecollections['sna_rbc_collection'] = None
    collection_29A45 = bpy.data.collections.new(name=Coll_Name, )
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection = collection_29A45
    collection_29A45.hide_select = False
    if Link:
        Link_Coll.children.link(child=collection_29A45, )
    else:
        bpy.context.scene.collection.children.link(child=collection_29A45, )
    rbc_scenecollections['sna_rbc_collection'] = collection_29A45
    return collection_29A45


def sna_link_collection_to_rbc_addon_collection_4AC89(Collection):
    if Collection in list(bpy.data.collections['RBC Addon'].children):
        pass
    else:
        bpy.data.collections['RBC Addon'].children.link(child=Collection, )
    if (Collection in list(bpy.data.collections['RBC Addon'].children) and Collection in list(bpy.context.scene.collection.children)):
        bpy.context.scene.collection.children.unlink(child=Collection, )


def sna_link_obj_B65F4(Obj, Collection):
    Collection.objects.link(object=Obj, )
    if bpy.context.scene.collection in bpy.context.view_layer.objects.active.users_collection:
        bpy.context.scene.collection.objects.unlink(object=Obj, )


def sna_hide_active_rig_constraints_F46AB():
    for i_FC9B1 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection)):
        if ('.RB' in bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_FC9B1].obj.name or '.RigControl' in bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_FC9B1].obj.name):
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_FC9B1].obj.hide_set(state=False, )
        else:
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_FC9B1].obj.hide_set(state=True, )


class SNA_OT_Offset_Active_Rig_Location_Op_3614B(bpy.types.Operator):
    bl_idname = "sna.offset_active_rig_location_op_3614b"
    bl_label = "Offset Active Rig Location OP"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_1AC93 in range(len(bpy.context.scene.sna_rbc_rig_collection)):
            if (i_1AC93 != bpy.context.scene.sna_rbc_rig_collection.find(bpy.context.scene.sna_active_rig)):
                obj1 = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[0].body_rb
                obj2 = bpy.context.scene.sna_rbc_rig_collection[i_1AC93].rig_bodies[0].body_rb
                cntrlrig = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj
                from mathutils.bvhtree import BVHTree
                # Get the objects
                # Get their world matrix
                mat1 = obj1.matrix_world
                mat2 = obj2.matrix_world
                # Get the geometry in world coordinates
                vert1 = [mat1 @ v.co for v in obj1.data.vertices] 
                poly1 = [p.vertices for p in obj1.data.polygons]
                vert2 = [mat2 @ v.co for v in obj2.data.vertices] 
                poly2 = [p.vertices for p in obj2.data.polygons]
                # Create the BVH trees
                bvh1 = BVHTree.FromPolygons( vert1, poly1 )
                bvh2 = BVHTree.FromPolygons( vert2, poly2 )
                # Test if overlap
                if bvh1.overlap( bvh2 ):
                    rig_control.location.x = rig_control.dimensions.x
                else:
                    pass
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_create_trailer_hitch_8BF57(Car_Body, Vehicle_Trailer, ID_Name):
    sna_create_rigid_body_constraint_4EDB9(Vehicle_Trailer, Car_Body, True, (0.0, 0.0, 0.0), Vehicle_Trailer.name.replace('.RB', '.Hitch'), 'GENERIC_SPRING', (True, True, False), (0.0, 0.0, -15.0, 15.0, 0.0, 0.0), (True, True, True), (0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (False, True, False), (0.0, 0.0, 100.0, 1.0, 0.0, 0.0), (False, False, False), (0.0, 0.0, 0.0, 0.0, 0.0, 0.0), True, True, False, 0.0, 'SPHERE', 1.0)
    sna_create_child_of_constraint_381B2(None, Vehicle_Trailer, False, True, True)
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])
    rigging_parts['sna_hitch_constraint'] = bpy.context.view_layer.objects.active


class SNA_OT_Remove_Constraints_Bc322(bpy.types.Operator):
    bl_idname = "sna.remove_constraints_bc322"
    bl_label = "Remove Constraints"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_EDDF5 in range(len(bpy.data.objects)):
            for i_91431 in range(len(bpy.data.objects[i_EDDF5].constraints)):
                if 'RBC' in bpy.data.objects[i_EDDF5].constraints[i_91431].name:
                    bpy.data.objects[i_EDDF5].constraints.remove(constraint=bpy.data.objects[i_EDDF5].constraints[i_91431], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_PT_NEW_PANEL_9119D(bpy.types.Panel):
    bl_label = 'New Panel'
    bl_idname = 'SNA_PT_NEW_PANEL_9119D'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_category = 'CONS'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (True)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        op = layout.operator('sna.remove_constraints_bc322', text='Remove Constraints', icon_value=0, emboss=True, depress=False)


def sna_create_rigid_body_constraint_4EDB9(OBJ_1, OBJ_2, Add_Constraint_OBJ, Contraint_OBJ_Loc, Contraint_Name, Constraint_Type, Enable_Ang_Limits, Ang_Limits, Enable_Lin_Limits, Lin_Limits, Enable_Ang_Springs, Ang_Springs, Enable_Lin_Springs, Lin_Springs, Enabled, Disable_Collisions, Brakeable, Brake_Threshold, Empty_Type, Empty_Size):
    if Add_Constraint_OBJ:
        bpy.ops.object.empty_add('INVOKE_DEFAULT', type='ARROWS', radius=1.0, location=Contraint_OBJ_Loc)
        bpy.context.view_layer.objects.active.name = Contraint_Name
        bpy.context.view_layer.objects.active.empty_display_type = Empty_Type
        bpy.context.view_layer.objects.active.empty_display_size = Empty_Size
    bpy.ops.rigidbody.constraint_add('INVOKE_DEFAULT', type=Constraint_Type)
    bpy.context.view_layer.objects.active.rigid_body_constraint.object1 = OBJ_1
    bpy.context.view_layer.objects.active.rigid_body_constraint.object2 = OBJ_2
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_limit_ang_x = Enable_Ang_Limits[0]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_limit_ang_y = Enable_Ang_Limits[1]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_limit_ang_z = Enable_Ang_Limits[2]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_limit_lin_x = Enable_Lin_Limits[0]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_limit_lin_y = Enable_Lin_Limits[1]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_limit_lin_z = Enable_Lin_Limits[2]
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_ang_x_lower = math.radians(Ang_Limits[0])
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_ang_x_upper = math.radians(Ang_Limits[1])
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_ang_y_lower = math.radians(Ang_Limits[2])
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_ang_y_upper = math.radians(Ang_Limits[3])
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_ang_z_lower = math.radians(Ang_Limits[4])
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_ang_z_upper = math.radians(Ang_Limits[5])
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_lin_x_lower = Lin_Limits[0]
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_lin_x_upper = Lin_Limits[1]
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_lin_y_lower = Lin_Limits[2]
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_lin_y_upper = Lin_Limits[3]
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_lin_z_lower = Lin_Limits[4]
    bpy.context.view_layer.objects.active.rigid_body_constraint.limit_lin_z_upper = Lin_Limits[5]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_spring_ang_x = Enable_Ang_Springs[0]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_spring_ang_y = Enable_Ang_Springs[1]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_spring_ang_z = Enable_Ang_Springs[2]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_spring_x = Enable_Lin_Springs[0]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_spring_y = Enable_Lin_Springs[1]
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_spring_z = Enable_Lin_Springs[2]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_stiffness_ang_x = Ang_Springs[0]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_damping_ang_x = Ang_Springs[1]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_stiffness_ang_y = Ang_Springs[2]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_damping_ang_y = Ang_Springs[3]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_stiffness_ang_z = Ang_Springs[4]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_damping_ang_z = Ang_Springs[5]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_stiffness_x = Lin_Springs[0]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_damping_x = Lin_Springs[1]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_stiffness_y = Lin_Springs[2]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_damping_y = Lin_Springs[3]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_stiffness_z = Lin_Springs[4]
    bpy.context.view_layer.objects.active.rigid_body_constraint.spring_damping_z = Lin_Springs[5]
    bpy.context.view_layer.objects.active.rigid_body_constraint.enabled = Enabled
    bpy.context.view_layer.objects.active.rigid_body_constraint.disable_collisions = Disable_Collisions
    bpy.context.view_layer.objects.active.rigid_body_constraint.use_breaking = Brakeable
    bpy.context.view_layer.objects.active.rigid_body_constraint.breaking_threshold = Brake_Threshold


def sna_vehicle_bed_constraint_E7265(Car_Body, Car_Bed, Vehicle_Prop):
    sna_create_rigid_body_constraint_4EDB9(Car_Bed, Car_Body, True, (0.0, 0.0, 0.0), Car_Bed.name.replace('.RB', '.Hitch'), 'GENERIC_SPRING', (True, True, True), (0.0, 0.0, -15.0, 15.0, 0.0, 0.0), (True, True, True), (0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (False, True, False), (0.0, 0.0, 100.0, 1.0, 0.0, 0.0), (False, False, False), (0.0, 0.0, 0.0, 0.0, 0.0, 0.0), True, True, False, 0.0, 'SPHERE', 1.0)
    sna_create_child_of_constraint_381B2(None, Car_Bed, False, True, True)
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])
    rigging_parts['sna_hitch_constraint'] = bpy.context.view_layer.objects.active
    Vehicle_Prop.body_hitch_obj = bpy.context.view_layer.objects.active


def sna_add_disable_constraint_B681C(Wheels, Body):
    bpy.ops.object.empty_add('INVOKE_DEFAULT', type='PLAIN_AXES', radius=0.5, align='WORLD', location=(0.0, 0.0, 0.0))
    bpy.ops.rigidbody.constraint_add('INVOKE_DEFAULT', type='FIXED')
    bpy.context.view_layer.objects.active.name = 'RBC Disable Constraint'
    bpy.context.view_layer.objects.active.rigid_body_constraint.object1 = Wheels
    bpy.context.view_layer.objects.active.rigid_body_constraint.object2 = Body
    bpy.context.view_layer.objects.active.rigid_body_constraint.enabled = False
    bpy.context.view_layer.objects.active.rigid_body_constraint.disable_collisions = True
    bpy.context.view_layer.objects.active.rigid_body_constraint.solver_iterations = 1
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])


def sna_wheel_constraint_C1AA1(RBC_Wheel, RBC_Car, Suspension_Limits, Sunspenion_Stiffness, Sunspenion_Damping, SteeringSpring_Boolean, SteeringSpring_Stiffness, SteeringSpring_Dampning, Steering_Angle, Loc, Wheel_Name, Name, Id_Name, Is_UpdateOnly):
    rigging_parts['sna_wheelconstraint'] = None
    sna_create_rigid_body_constraint_4EDB9(RBC_Car, RBC_Wheel, True, (0.0, 0.0, 0.0), RBC_Wheel.name.replace('.RB', Name), 'GENERIC_SPRING', (False, True, True), (0.0, 0.0, 0.0, 0.0, float(Steering_Angle * -1.0), Steering_Angle), (True, True, True), (0.0, 0.0, 0.0, 0.0, float(float(Suspension_Limits / 4.0) * -1.0), Suspension_Limits), (False, False, True), (0.0, 0.0, 0.0, 0.0, SteeringSpring_Stiffness, SteeringSpring_Dampning), (False, False, True), (0.0, 0.0, 0.0, 0.0, Sunspenion_Stiffness, Sunspenion_Damping), True, True, False, 0.0, 'ARROWS', 1.0)
    sna_create_child_of_constraint_381B2(None, RBC_Wheel, False, False, False)
    sna_add_to_rig_obj_collection_31032()
    rigging_parts['sna_wheelconstraint'] = bpy.context.view_layer.objects.active
    sna_hide_obj_select_71598(rigging_parts['sna_wheelconstraint'], True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])


def sna_create_child_of_constraint_381B2(OBJ, OBJ_constrained_to, Input, Hitch, Use_group):
    constraint_38878 = bpy.context.view_layer.objects.active.constraints.new(type='CHILD_OF', )
    constraint_38878.name = 'Child Of RB Wheel'
    constraint_38878.target = OBJ_constrained_to
    if Use_group:
        constraint_38878.subtarget = 'RBC Group'
    if Input:
        constraint_38878.use_rotation_z = False
    if Hitch:
        constraint_38878.use_rotation_z = True
        constraint_38878.use_rotation_x = False
        constraint_38878.use_rotation_y = False


def sna_rbc_motor_constraints_D0C93(RBC_Wheel, RBC_Car, Name, Constraint_Name, Is_Steering, Loc, Enabled, Is_Update_Only):
    bpy.ops.object.empty_add('INVOKE_DEFAULT', type='ARROWS', radius=1.0, location=Loc)
    bpy.context.view_layer.objects.active.name = Name.replace('.RB', Constraint_Name)
    bpy.ops.rigidbody.constraint_add('INVOKE_DEFAULT', type='MOTOR')
    bpy.data.objects[Name.replace('.RB', Constraint_Name)].rigid_body_constraint.enabled = Enabled
    bpy.data.objects[Name.replace('.RB', Constraint_Name)].rigid_body_constraint.use_motor_ang = True
    if Is_Steering:
        bpy.data.objects[Name.replace('.RB', Constraint_Name)].rigid_body_constraint.object1 = RBC_Wheel
        bpy.data.objects[Name.replace('.RB', Constraint_Name)].rigid_body_constraint.object2 = RBC_Car
    else:
        bpy.data.objects[Name.replace('.RB', Constraint_Name)].rigid_body_constraint.object2 = RBC_Wheel
        bpy.data.objects[Name.replace('.RB', Constraint_Name)].rigid_body_constraint.object1 = RBC_Car
    if Is_Steering:
        bpy.data.objects[Name.replace('.RB', Constraint_Name)].delta_rotation_euler = (0.0, math.radians(90.0), 0.0)
        rigging_parts['sna_wheelsteeringmotor'] = bpy.context.view_layer.objects.active
    else:
        rigging_parts['sna_wheelmotor'] = bpy.context.view_layer.objects.active
    sna_create_child_of_constraint_381B2(None, RBC_Wheel, False, False, False)
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])


def sna_create_roll_constraint_20E71(Vehicle_Body, ID_Name, Body_Prop):
    sna_create_rigid_body_constraint_4EDB9((None if (bpy.context.scene.sna_rbc_scene_.ground == None) else bpy.context.scene.sna_rbc_scene_.ground), Vehicle_Body, True, (0.0, 0.0, 0.0), Vehicle_Body.name.replace('.RB', '.Roll_Constraint'), 'GENERIC_SPRING', (True, True, False), (-45.0, 45.0, -10.0, 10.0, 0.0, 0.0), (False, False, False), (0.0, 0.0, 0.0, 0.0, 0.0, 0.0), (True, True, False), (100.0, 2.0, 100.0, 2.0, 0.0, 0.0), (False, False, False), (0.0, 0.0, 0.0, 0.0, 0.0, 0.0), False, False, False, 0.0, 'ARROWS', 1.0)
    Body_Prop.physics_roll_constraint = bpy.context.view_layer.objects.active
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])
    sna_create_child_of_constraint_381B2(bpy.context.view_layer.objects.active, Vehicle_Body, True, False, False)


def sna_create_lean_constraint_A4F6A(Vehicle_Body, ID_Name, Body_Prop):
    bpy.ops.object.empty_add('INVOKE_DEFAULT', type='ARROWS', radius=1.0, location=(0.0, 0.0, 0.0))
    bpy.context.view_layer.objects.active.name = Vehicle_Body.name.replace('.RB', '.Lean_Constraint')
    bpy.data.objects[Vehicle_Body.name.replace('.RB', '.Lean_Constraint')].delta_rotation_euler = (0.0, 0.0, math.radians(90.0))
    Body_Prop.physics_lean_constraint = bpy.context.view_layer.objects.active
    bpy.ops.rigidbody.constraint_add('INVOKE_DEFAULT', type='MOTOR')
    bpy.data.objects[Vehicle_Body.name.replace('.RB', '.Lean_Constraint')].rigid_body_constraint.disable_collisions = False
    bpy.data.objects[Vehicle_Body.name.replace('.RB', '.Lean_Constraint')].rigid_body_constraint.enabled = False
    bpy.data.objects[Vehicle_Body.name.replace('.RB', '.Lean_Constraint')].rigid_body_constraint.use_motor_ang = True
    bpy.data.objects[Vehicle_Body.name.replace('.RB', '.Lean_Constraint')].rigid_body_constraint.object1 = (None if (bpy.context.scene.sna_rbc_scene_.ground == None) else bpy.context.scene.sna_rbc_scene_.ground)
    bpy.data.objects[Vehicle_Body.name.replace('.RB', '.Lean_Constraint')].rigid_body_constraint.object2 = Vehicle_Body
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])
    sna_create_child_of_constraint_381B2(bpy.context.view_layer.objects.active, Vehicle_Body, True, False, False)


def sna_add_to_rbc_wheels_collection_2BBCA(Wheel_Coll_Prop, Wheel_RB, Wheel_Constraint, Wheel_SteeringMotor, Wheel_Motor, Axle_Index, Car_Body_, Camber_Tilt_Obj, Brake_Caliper_Obj):
    Wheel_Coll_Prop.wheel_rb = Wheel_RB
    Wheel_Coll_Prop.wheel_constraint = Wheel_Constraint
    Wheel_Coll_Prop.wheel_steeringmotor = Wheel_SteeringMotor
    Wheel_Coll_Prop.wheel_motor = Wheel_Motor
    Wheel_Coll_Prop.wheel_brakecaliper_obj = Brake_Caliper_Obj
    Wheel_Coll_Prop.wheel_cambertilt_obj = Camber_Tilt_Obj
    Wheel_Coll_Prop.name = str(Wheel_Coll_Prop)


def sna_create_trailer_F4A92(ID_Name, Prop, Car_Body, Trailers, Axles, Input_001):
    for i_A3BF3 in range(Trailers):
        car_body_0_d5d74, vehicle_body_id_1_d5d74 = sna_create_car_body_2379B('Vehicle Trailer', Prop, False, None, ID_Name)
        sna_create_trailer_hitch_8BF57(Car_Body, car_body_0_d5d74, ID_Name)
        vehicle_body_id_1_d5d74.body_hitch_obj = bpy.context.view_layer.objects.active
        sna_create_rbc_axle_5CDFD('TA', ID_Name, 2, 'Dead', car_body_0_d5d74, Axles, False)
        return car_body_0_d5d74


def sna_create_disable_constraints_28638(Bed_Exists, Index):
    if Bed_Exists:
        for i_E02D0 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
            for i_69BDC in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection)):
                if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_69BDC].obj.rigid_body == None):
                    pass
                else:
                    Variable_1 = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_69BDC].obj
                    Variable_2 = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E02D0].body_rb
                    Bool = None
                    from mathutils.bvhtree import BVHTree
                    # Get the objects
                    obj1 = Variable_1
                    obj2 = Variable_2
                    Bool = bpy.context.scene.sna_overlap_bool
                    # Get their world matrix
                    mat1 = obj1.matrix_world
                    mat2 = obj2.matrix_world
                    # Get the geometry in world coordinates
                    vert1 = [mat1 @ v.co for v in obj1.data.vertices] 
                    poly1 = [p.vertices for p in obj1.data.polygons]
                    vert2 = [mat2 @ v.co for v in obj2.data.vertices] 
                    poly2 = [p.vertices for p in obj2.data.polygons]
                    # Create the BVH trees
                    bvh1 = BVHTree.FromPolygons( vert1, poly1 )
                    bvh2 = BVHTree.FromPolygons( vert2, poly2 )
                    # Test if overlap
                    if bvh1.overlap( bvh2 ):
                        Bool = True
                    else:
                        Bool = False
                    if Bool:
                        sna_add_disable_constraint_B681C(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_69BDC].obj, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E02D0].body_rb)


def sna_add_rb_wheel_E7F9E(Name, ID):
    rigging_parts['sna_wheelrb'] = None
    bpy.ops.mesh.primitive_cylinder_add('INVOKE_DEFAULT', vertices=16, radius=1.0, enter_editmode=True, location=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 0.5))
    group_516AF = bpy.context.view_layer.objects.active.vertex_groups.new(name='RBC Group', )
    bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
    bpy.ops.object.vertex_group_assign('INVOKE_DEFAULT', )
    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
    bpy.ops.rigidbody.object_add('INVOKE_DEFAULT', type='ACTIVE')
    bpy.context.view_layer.objects.active.rigid_body.collision_shape = 'CYLINDER'
    bpy.context.view_layer.objects.active.rigid_body.enabled = False
    bpy.context.view_layer.objects.active.rigid_body.collision_collections = (False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    bpy.context.view_layer.objects.active.rigid_body.mass = 0.10000000149011612
    bpy.context.view_layer.objects.active.rigid_body.friction = 5.0
    bpy.context.view_layer.objects.active.delta_rotation_euler = (0.0, math.radians(90.0), 0.0)
    bpy.context.view_layer.objects.active.name = Name + '_Wheel.RB'
    bpy.data.objects[bpy.context.view_layer.objects.active.name].display_type = 'WIRE'
    sna_add_to_rig_obj_collection_31032()
    rigging_parts['sna_wheelrb'] = bpy.context.view_layer.objects.active
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, False, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])
    return Name + '_Wheel.RB'


def sna_create_car_body_2379B(Name, Prop, is_CarBody_2, Car_Body, Id_Name):
    item_93BF1 = Prop.rig_bodies.add()
    item_93BF1.name = Name
    sna_add_rbc_car_body_11DFA(Name, Id_Name)
    item_93BF1.body_rb = bpy.context.view_layer.objects.active
    rigging_parts['sna_car_body'] = bpy.context.view_layer.objects.active
    return [item_93BF1.body_rb, item_93BF1]


def sna_add_rbc_car_body_11DFA(Name, ID_name):
    bpy.ops.mesh.primitive_cube_add('INVOKE_DEFAULT', location=(0.0, 0.0, 0.0))
    bpy.ops.rigidbody.object_add('INVOKE_DEFAULT', type='ACTIVE')
    bpy.context.view_layer.objects.active.rigid_body.enabled = False
    bpy.context.view_layer.objects.active.rigid_body.collision_collections = (False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
    bpy.context.view_layer.objects.active.name = ID_name + '.' + Name + '.RB'
    bpy.context.view_layer.objects.active.display_type = 'WIRE'
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, False, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])


def sna_create_rbc_wheels_collection_68B29(Axle_Index, Body_Prop):
    item_FE71B = Body_Prop.sna_body_axles[Axle_Index].axle_wheels.add()
    return [item_FE71B, list(Body_Prop.sna_body_axles[Axle_Index].axle_wheels).index(item_FE71B)]


def sna_create_rbc_wheel_49AE9(Name, ID, Int, is_Steering, Is_Drive, Car_Body, Axle_Index, Input):
    for i_697EC in range(Int):
        wheel_coll_prop_0_8e534, wheel_coll_index_1_8e534 = sna_create_rbc_wheels_collection_68B29(Axle_Index, Car_Body)
        wheel_name_0_323a5 = sna_add_rb_wheel_E7F9E(Name + ('L' if (wheel_coll_index_1_8e534 == 1) else 'R') + str(wheel_coll_index_1_8e534), str(wheel_coll_index_1_8e534))
        sna_wheel_constraint_C1AA1(rigging_parts['sna_wheelrb'], Car_Body, 1.0, 100.0, 5.0, is_Steering, 150.0, 50.0, (35.0 if is_Steering else 0.0), bpy.context.view_layer.objects.active.location, wheel_name_0_323a5, '_Constraint', '1', False)
        sna_rbc_motor_constraints_D0C93(rigging_parts['sna_wheelrb'], Car_Body, wheel_name_0_323a5, '_Motor', False, bpy.context.view_layer.objects.active.location, (True if Is_Drive else False), None)
        sna_rbc_motor_constraints_D0C93(rigging_parts['sna_wheelrb'], Car_Body, wheel_name_0_323a5, '_SteeringMotor', True, bpy.context.view_layer.objects.active.location, (True if is_Steering else False), None)
        sna_create_camber_obj_F60E0(wheel_name_0_323a5, Car_Body)
        sna_create_break_caliper_D3A22(wheel_name_0_323a5, rigging_parts['sna_wheelrb'], rigging_parts['sna_wheelcambertilt'])
        sna_add_to_rbc_wheels_collection_2BBCA(wheel_coll_prop_0_8e534, rigging_parts['sna_wheelrb'], rigging_parts['sna_wheelconstraint'], rigging_parts['sna_wheelsteeringmotor'], rigging_parts['sna_wheelmotor'], Axle_Index, Car_Body, rigging_parts['sna_wheelcambertilt'], rigging_parts['sna_wheelbrakecaliper'])


def sna_create_rbc_axle_5CDFD(Name, Name_ID, Wheels, Axle_Type, Car_Body, Axles, Only_Axles):
    for i_E82A9 in range(Axles):
        item_A8528 = Car_Body.sna_body_axles.add()
        item_A8528.name = str(item_A8528)
        item_A8528.axle_type = Axle_Type
        if Only_Axles:
            pass
        else:
            if Axle_Type == "Drive":
                sna_create_rbc_wheel_49AE9(Name_ID + '.' + ('Trailer' if 'Trailer' in Car_Body.name else ('Bed' if 'Bed' in Car_Body.name else 'Body')) + '.' + str(list(Car_Body.sna_body_axles).index(item_A8528)) + ('.B' if (list(Car_Body.sna_body_axles).index(item_A8528) > 0) else '.F'), str(list(Car_Body.sna_body_axles).index(item_A8528)), Wheels, False, True, Car_Body, item_A8528.name, None)
            elif Axle_Type == "Steering":
                sna_create_rbc_wheel_49AE9(Name_ID + '.' + ('Trailer' if 'Trailer' in Car_Body.name else ('Bed' if 'Bed' in Car_Body.name else 'Body')) + '.' + str(list(Car_Body.sna_body_axles).index(item_A8528)) + ('.B' if (list(Car_Body.sna_body_axles).index(item_A8528) > 0) else '.F'), str(list(Car_Body.sna_body_axles).index(item_A8528)), Wheels, True, False, Car_Body, item_A8528.name, None)
            elif Axle_Type == "Drive/Steering":
                sna_create_rbc_wheel_49AE9(Name_ID + '.' + ('Trailer' if 'Trailer' in Car_Body.name else ('Bed' if 'Bed' in Car_Body.name else 'Body')) + '.' + str(list(Car_Body.sna_body_axles).index(item_A8528)) + ('.B' if (list(Car_Body.sna_body_axles).index(item_A8528) > 0) else '.F'), str(list(Car_Body.sna_body_axles).index(item_A8528)), Wheels, True, True, Car_Body, item_A8528.name, None)
            elif Axle_Type == "Dead":
                sna_create_rbc_wheel_49AE9(Name_ID + '.' + ('Trailer' if 'Trailer' in Car_Body.name else ('Bed' if 'Bed' in Car_Body.name else 'Body')) + '.' + str(list(Car_Body.sna_body_axles).index(item_A8528)) + ('.B' if (list(Car_Body.sna_body_axles).index(item_A8528) > 0) else '.F'), str(list(Car_Body.sna_body_axles).index(item_A8528)), Wheels, False, False, Car_Body, item_A8528.name, None)
            else:
                pass


def sna_create_camber_obj_F60E0(ID_Name, Vehicle_Body):
    rigging_parts['sna_wheelcambertilt'] = None
    bpy.ops.object.empty_add('INVOKE_DEFAULT', type='PLAIN_AXES', location=(0.0, 0.0, 0.0))
    bpy.context.view_layer.objects.active.name = ID_Name.replace('.RB', '_CamberTilt')
    rigging_parts['sna_wheelcambertilt'] = bpy.context.view_layer.objects.active
    constraint_8C051 = bpy.context.view_layer.objects.active.constraints.new(type='CHILD_OF', )
    constraint_8C051.name = 'RBC Child Of RB Vehicle'
    constraint_8C051.target = Vehicle_Body
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])


def sna_create_break_caliper_D3A22(ID_Name, Wheel, Camber_Angle):
    rigging_parts['sna_wheelbrakecaliper'] = None
    bpy.ops.object.empty_add('INVOKE_DEFAULT', type='PLAIN_AXES', radius=0.5, location=(0.0, 0.0, 0.0))
    bpy.context.view_layer.objects.active.name = ID_Name.replace('.RB', '_BrakeCaliper')
    rigging_parts['sna_wheelbrakecaliper'] = bpy.context.view_layer.objects.active
    constraint_E611C = bpy.context.view_layer.objects.active.constraints.new(type='CHILD_OF', )
    constraint_E611C.name = 'RBC Child Of RB Wheel'
    constraint_E611C.target = Wheel
    constraint_7EB8A = bpy.context.view_layer.objects.active.constraints.new(type='COPY_ROTATION', )
    constraint_7EB8A.name = 'RBC Copy Rot Camber Angle'
    constraint_7EB8A.target = Camber_Angle
    constraint_7EB8A.use_z = False
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, True, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])


def sna_add_rbc_rig_control_5F8F2(ID_Name, Rig_Name, Prop):
    bpy.ops.mesh.primitive_plane_add('INVOKE_DEFAULT', size=5.0, enter_editmode=True, location=(0.0, 0.0, 0.0), scale=(2.0, 2.0, 3.0))
    bpy.ops.mesh.delete('INVOKE_DEFAULT', type='ONLY_FACE')
    bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
    bpy.ops.transform.translate(value=(0, 0, 0.15), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
    modifier_655C4 = bpy.context.view_layer.objects.active.modifiers.new(name='', type='BEVEL', )
    modifier_655C4.affect = 'VERTICES'
    modifier_655C4.width = 0.25
    modifier_655C4.segments = 4
    bpy.context.view_layer.objects.active.name = ID_Name + Rig_Name
    Prop.rig_control_obj = bpy.context.view_layer.objects.active
    sna_add_to_rig_obj_collection_31032()
    sna_hide_obj_select_71598(bpy.context.view_layer.objects.active, True, False, False, False)
    sna_link_obj_B65F4(bpy.context.view_layer.objects.active, rbc_scenecollections['sna_rbc_collection'])
    return Prop.rig_control_obj


def sna_add_to_rig_obj_collection_31032():
    item_6DF18 = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection.add()
    item_6DF18.name = bpy.context.view_layer.objects.active.name
    item_6DF18.obj = bpy.context.view_layer.objects.active


def sna_create_rbc_rig_prop_9B9C6():
    item_F95DC = bpy.context.scene.sna_rbc_rig_collection.add()
    item_F95DC.name = str(random_integer(0.0, 10.0, None)) + str(random_integer(0.0, 10.0, None)) + str(random_integer(0.0, 10.0, None)) + str(random_integer(0.0, 10.0, None))
    bpy.context.scene.sna_active_rig = item_F95DC.name
    bpy.context.scene.sna_rbc_collection_list = item_F95DC.name
    item_F95DC.rig_type = bpy.context.scene.sna_rbc_rig_type_menu
    bpy.context.scene.sna_rbc_rig_collection[item_F95DC.name].rig_drivers.name = item_F95DC.name
    item_F95DC.rig_name = item_F95DC.name + ' Rig'
    return [item_F95DC.name, item_F95DC.name, bpy.context.scene.sna_rbc_rig_collection[item_F95DC.name]]


def sna_create_vehicle_body_AD0C5(Prop, Has_Bed, ID_Name):
    car_body_0_01bcf, vehicle_body_id_1_01bcf = sna_create_car_body_2379B('Vehicle Body', Prop, False, None, ID_Name)
    sna_create_roll_constraint_20E71(car_body_0_01bcf, ID_Name, vehicle_body_id_1_01bcf)
    sna_create_lean_constraint_A4F6A(car_body_0_01bcf, ID_Name, vehicle_body_id_1_01bcf)
    if Has_Bed:
        car_body_0_293f8, vehicle_body_id_1_293f8 = sna_create_car_body_2379B('Vehicle Bed', Prop, True, car_body_0_01bcf, ID_Name)
        sna_create_roll_constraint_20E71(car_body_0_293f8, ID_Name, vehicle_body_id_1_293f8)
        sna_vehicle_bed_constraint_E7265(car_body_0_01bcf, car_body_0_293f8, vehicle_body_id_1_293f8)
    return [car_body_0_01bcf, (car_body_0_293f8 if Has_Bed else car_body_0_01bcf)]


def sna_hide_obj_select_71598(OBJ, Enable, Hide, Render, Ray_Visability):
    OBJ.hide_select = Enable
    OBJ.hide_render = (not Render)
    OBJ.hide_set(state=Hide, )
    sna_disable_ray_visablilty_B5A59(OBJ, Ray_Visability)


def sna_add_to_physics_pt_add_1E465(self, context):
    if not (False):
        layout = self.layout


def sna_add_to_physics_pt_rigid_body_constraint_objects_E7853(self, context):
    if not (True):
        layout = self.layout
        row_45289 = layout.row(heading='', align=False)
        row_45289.alert = False
        row_45289.enabled = True
        row_45289.active = True
        row_45289.use_property_split = False
        row_45289.use_property_decorate = False
        row_45289.scale_x = 1.0
        row_45289.scale_y = 1.0
        row_45289.alignment = 'Center'.upper()
        row_45289.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = row_45289.operator('sna.switch_objects_8b723', text='Switch Objects', icon_value=0, emboss=True, depress=False)


class SNA_OT_Copy_Selected_Constraints_9629A(bpy.types.Operator):
    bl_idname = "sna.copy_selected_constraints_9629a"
    bl_label = "Copy Selected Constraints"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Switch_Objects_8B723(bpy.types.Operator):
    bl_idname = "sna.switch_objects_8b723"
    bl_label = "Switch Objects"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        rigid_body_tools['sna_obj_1'] = None
        rigid_body_tools['sna_obj_2'] = None
        rigid_body_tools['sna_obj_1'] = bpy.context.view_layer.objects.active.rigid_body_constraint.object1
        rigid_body_tools['sna_obj_2'] = bpy.context.view_layer.objects.active.rigid_body_constraint.object2
        bpy.context.view_layer.objects.active.rigid_body_constraint.object1 = rigid_body_tools['sna_obj_2']
        bpy.context.view_layer.objects.active.rigid_body_constraint.object2 = rigid_body_tools['sna_obj_1']
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_set_weight_4C3C1(OBJ):
    OBJ.rigid_body.mass = round(eval("OBJ.dimensions[0] + OBJ.dimensions[1] + OBJ.dimensions[2] / 3"), abs(2))


class SNA_OT_Clear_Rig_Control_Constraints_2322E(bpy.types.Operator):
    bl_idname = "sna.clear_rig_control_constraints_2322e"
    bl_label = "Clear Rig Control Constraints"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_D25D7 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection)):
            if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_D25D7].obj.constraints['RBC Child Of Rig Control']", globals(), locals()):
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_D25D7].obj.constraints.remove(constraint=bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_D25D7].obj.constraints['RBC Child Of Rig Control'], )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Rb_Obj_Buttons_2603E(bpy.types.Operator):
    bl_idname = "sna.reset_rb_obj_buttons_2603e"
    bl_label = "Reset RB OBJ Buttons"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_C3C5F in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_collection = None
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_model = None
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_button = False
            for i_799CC in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_rb.sna_body_axles)):
                for i_DC52F in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_rb.sna_body_axles[i_799CC].axle_wheels)):
                    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_rb.sna_body_axles[i_799CC].axle_wheels[i_DC52F].wheel_collection = None
                    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_rb.sna_body_axles[i_799CC].axle_wheels[i_DC52F].wheel_model = None
                    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_rb.sna_body_axles[i_799CC].axle_wheels[i_DC52F].wheel_button = False
                    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_C3C5F].body_rb.sna_body_axles[i_799CC].axle_wheels[i_DC52F].wheel_extra_button = False
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Reset_Rb_Obj_Location_D2903(bpy.types.Operator):
    bl_idname = "sna.reset_rb_obj_location_d2903"
    bl_label = "Reset RB OBJ Location"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_53247 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection)):
            if (not (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_53247].obj == None)):
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_53247].obj.location = (0.0, 0.0, 0.0)
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_obj_collection[i_53247].obj.rotation_euler = (0.0, 0.0, 0.0)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_parent_rig_DDFCF():
    for i_3ED0E in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
        constraint_BE797 = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_3ED0E].body_rb.constraints.new(type='CHILD_OF', )
        constraint_BE797.target = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj
        constraint_BE797.name = 'RBC Child Of Rig Control'
        for i_5CC4A in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_3ED0E].body_rb.sna_body_axles)):
            for i_A1501 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_3ED0E].body_rb.sna_body_axles[i_5CC4A].axle_wheels)):
                constraint_9983B = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_3ED0E].body_rb.sna_body_axles[i_5CC4A].axle_wheels[i_A1501].wheel_rb.constraints.new(type='CHILD_OF', )
                constraint_9983B.target = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj
                constraint_9983B.name = 'RBC Child Of Rig Control'


def sna_add_to_rbc_model_collection_CBFB5(OBJ):
    item_867F8 = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection.add()
    item_867F8.obj = OBJ
    item_867F8.name = str(item_867F8.obj.name)


def sna_enable_rb_D11F3(Enabled):
    for i_69A23 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.rigid_body.enabled = Enabled
        if Enabled:
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.rigid_body.collision_collections = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
        else:
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.rigid_body.collision_collections = (False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
        for i_934D2 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.sna_body_axles)):
            for i_4B747 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.sna_body_axles[i_934D2].axle_wheels)):
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.sna_body_axles[i_934D2].axle_wheels[i_4B747].wheel_rb.rigid_body.enabled = Enabled
                if Enabled:
                    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.sna_body_axles[i_934D2].axle_wheels[i_4B747].wheel_rb.rigid_body.collision_collections = (True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False)
                else:
                    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_69A23].body_rb.sna_body_axles[i_934D2].axle_wheels[i_4B747].wheel_rb.rigid_body.collision_collections = (False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False)


def sna_is_rigged_EDA15(T_F):
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_rigged = T_F
    if T_F:
        bpy.context.scene.sna_rbc_rig_panel = set(['Tuning'])
        bpy.context.scene.sna_rbc_collection_list = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_rbc_collection_list].name
        sna_activate_all_DF607(True)


def sna_parent_model_422C0(OBJ, RB_OBJ, Camber_Tilt_Obj, Wheel_Index, Has_Camber_Tilt):
    constraint_645D6 = OBJ.constraints.new(type='CHILD_OF', )
    constraint_645D6.target = RB_OBJ
    constraint_645D6.name = 'RBC Child Of'
    constraint_645D6.subtarget = 'RBC Group'
    if Has_Camber_Tilt:
        constraint_03D9D = OBJ.constraints.new(type='COPY_ROTATION', )
        constraint_03D9D.name = 'RBC Camber Tilt'
        constraint_03D9D.target = Camber_Tilt_Obj
        constraint_03D9D.use_x = False
        constraint_03D9D.use_z = False
        constraint_03D9D.use_y = False
    sna_add_to_rbc_model_collection_CBFB5(OBJ)


def sna_parent_collection_A5C77(Collection, RB_OBJ):
    for i_6A15F in range(len(Collection.objects)):
        if ((Collection.objects[i_6A15F].parent == None) and (not property_exists("Collection.objects[i_6A15F].constraints['RBC Child Of Brake Caliper']", globals(), locals()))):
            constraint_16D67 = Collection.objects[i_6A15F].constraints.new(type='CHILD_OF', )
            constraint_16D67.target = RB_OBJ
            constraint_16D67.name = 'RBC Child Of Model'
            sna_add_to_rbc_model_collection_CBFB5(Collection.objects[i_6A15F])


class SNA_OT_Parent_Modelcollection_28104(bpy.types.Operator):
    bl_idname = "sna.parent_modelcollection_28104"
    bl_label = "Parent Model/Collection"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_27224 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
            if (not (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_collection == None)):
                sna_parent_collection_A5C77(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_collection, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_boundingbox)
                bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_model = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_boundingbox
                sna_parent_model_422C0(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_model, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb, None, 0, False)
            else:
                sna_parent_model_422C0(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_model, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb, None, 0, False)
            for i_B21A6 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles)):
                for i_6BC4F in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels)):
                    if (not (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_collection == None)):
                        sna_parent_collection_A5C77(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_collection, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_boundingbox)
                        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_model = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_boundingbox
                        sna_parent_model_422C0(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_model, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_rb, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_cambertilt_obj, i_6BC4F, True)
                    else:
                        sna_parent_model_422C0(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_model, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_rb, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_27224].body_rb.sna_body_axles[i_B21A6].axle_wheels[i_6BC4F].wheel_cambertilt_obj, i_6BC4F, True)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_hide_vb_obj_select_8933E():
    for i_E73CC in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
        sna_hide_obj_select_71598(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E73CC].body_rb, True, False, False, False)


def sna_set_control_rig_499AB():
    bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
    for i_52FBD in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
        sna_hide_obj_select_71598(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_52FBD].body_rb, False, False, False, False)
        bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_52FBD].body_rb.select_set(state=True, )
    import bmesh
    import mathutils
    # from blender templates

    def add_box(width, height, depth):
        """
        This function takes inputs and returns vertex and face arrays.
        no actual mesh data creation is done here.
        """
        verts = [(+1.0, +1.0, -1.0),
                 (+1.0, -1.0, -1.0),
                 (-1.0, -1.0, -1.0),
                 (-1.0, +1.0, -1.0),
                 (+1.0, +1.0, +1.0),
                 (+1.0, -1.0, +1.0),
                 (-1.0, -1.0, +1.0),
                 (-1.0, +1.0, +1.0),
                 ]
        faces = [(0, 1, 2, 3),
                 (4, 7, 6, 5),
                 (0, 4, 5, 1),
                 (1, 5, 6, 2),
                 (2, 6, 7, 3),
                 (4, 0, 3, 7),
                ]
        # apply size
        for i, v in enumerate(verts):
            verts[i] = v[0] * width, v[1] * depth, v[2] * height
        return verts, faces

    def group_bounding_box():
        minx, miny, minz = (999999.0,)*3
        maxx, maxy, maxz = (-999999.0,)*3
        location = [0.0,]*3
        for obj in bpy.context.selected_objects:
            for v in obj.bound_box:
                v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))
                if v_world[0] < minx:
                    minx = v_world[0]
                if v_world[0] > maxx:
                    maxx = v_world[0]
                if v_world[1] < miny:
                    miny = v_world[1]
                if v_world[1] > maxy:
                    maxy = v_world[1]
                if v_world[2] < minz:
                    minz = v_world[2]
                if v_world[2] > maxz:
                    maxz = v_world[2]
        verts_loc, faces = add_box((maxx-minx)/2, (maxz-minz)/2, (maxy-miny)/2)
        mesh = bpy.data.meshes.new("BoundingBox")
        bm = bmesh.new()
        for v_co in verts_loc:
            bm.verts.new(v_co)
        bm.verts.ensure_lookup_table()
        for f_idx in faces:
            bm.faces.new([bm.verts[i] for i in f_idx])
        bm.to_mesh(mesh)
        mesh.update()
        location[0] = minx+((maxx-minx)/2)
        location[1] = miny+((maxy-miny)/2)
        location[2] = minz+((maxz-minz)/2)
        bbox = object_utils.object_data_add(bpy.context, mesh, operator=None)
        # does a bounding box need to display more than the bounds??
        bbox.location = location
        bbox.display_type = 'BOUNDS'
        bbox.hide_render = True
    group_bounding_box()
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location = bpy.context.view_layer.objects.active.location
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.dimensions = tuple(mathutils.Vector(bpy.context.view_layer.objects.active.dimensions) * mathutils.Vector((1.25, 1.0499999523162842, 1.0)))
    bpy.data.meshes.remove(mesh=bpy.context.view_layer.objects.active.data, )
    sna_apply_transform_B3258(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj)
    sna_hide_vb_obj_select_8933E()


def sna_adjust_rig_control_B567B():
    wheels_rb_0_e9f28 = sna_active_wheel_rb_list_DFE0F()
    Wheels = wheels_rb_0_e9f28
    sorted_objectz = None
    # Get the selected objects
    selected_objects = Wheels
    # Sort the selected objects by their x and y coordinates
    sorted_objectz = sorted(selected_objects, key=lambda obj: (round(obj.location.z, 1)))
    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location = (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location[0], bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location[1], float(sorted_objectz[0].location[2] + float(float(sorted_objectz[0].dimensions[0] / 2.0) * -1.0)))
    sna_hide_obj_select_71598(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj, False, False, False, False)


class SNA_OT_Clear_Rig_4Ed9B(bpy.types.Operator):
    bl_idname = "sna.clear_rig_4ed9b"
    bl_label = "Clear Rig"
    bl_description = "Resets Setup proccess of RBC rig"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        bpy.ops.sna.clear_model_constraints_43579('INVOKE_DEFAULT', )
        bpy.ops.sna.reset_rb_obj_buttons_2603e('INVOKE_DEFAULT', )
        bpy.ops.sna.reset_rb_obj_location_d2903('INVOKE_DEFAULT', )
        sna_enable_rb_D11F3(False)
        bpy.ops.sna.clear_rig_control_constraints_2322e('INVOKE_DEFAULT', )
        sna_reset_carrb_mesh_23CA0()
        sna_is_rigged_EDA15(False)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_set_wheel_constraint_0F00E(RB_OBJ, Constraint_OBJ, Weight):
    Constraint_OBJ.empty_display_size = float(RB_OBJ.dimensions[1] / 2.0)
    Constraint_OBJ.rigid_body_constraint.limit_lin_z_upper = float(RB_OBJ.dimensions[1] / 2.0)
    Constraint_OBJ.rigid_body_constraint.limit_lin_z_lower = float(float(float(RB_OBJ.dimensions[1] / 2.0) / 4.0) * -1.0)


class SNA_OT_Clear_Model_Constraints_43579(bpy.types.Operator):
    bl_idname = "sna.clear_model_constraints_43579"
    bl_label = "Clear Model Constraints"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_20AF4 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection)):
            set_up_generate_rig['sna_clear_constraints_list'] = []
            if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection[i_20AF4].obj != None):
                for i_FCAE0 in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection[i_20AF4].obj.constraints)):
                    if 'RBC' in bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection[i_20AF4].obj.constraints[i_FCAE0].name:
                        set_up_generate_rig['sna_clear_constraints_list'].append(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection[i_20AF4].obj.constraints[i_FCAE0])
                for i_00DAD in range(len(set_up_generate_rig['sna_clear_constraints_list'])):
                    bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection[i_20AF4].obj.constraints.remove(constraint=set_up_generate_rig['sna_clear_constraints_list'][i_00DAD], )
        if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection.sna_rbc_asset_collection if property_exists("bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_collection.sna_rbc_asset_collection", globals(), locals()) else False):
            pass
        else:
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_model_collection.clear()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Generate_Rig_6C502(bpy.types.Operator):
    bl_idname = "sna.generate_rig_6c502"
    bl_label = "Generate Rig"
    bl_description = "Generates RBC rig"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.ops.screen.frame_jump('INVOKE_DEFAULT', )
        bpy.ops.sna.create_convex_hull_78b8a('INVOKE_DEFAULT', )
        sna_set_control_rig_499AB()
        sna_adjust_rig_control_B567B()
        sna_enable_rb_D11F3(True)
        bpy.ops.sna.parent_modelcollection_28104('INVOKE_DEFAULT', )
        sna_parent_rig_DDFCF()
        sna_is_rigged_EDA15(True)
        bpy.ops.sna.snap_to_ground_f6c01('INVOKE_DEFAULT', )
        bpy.ops.sna.rig_tune_up_be9a4('INVOKE_DEFAULT', )
        bpy.ops.sna.transfer_rbc_rig_props_to_collection_8e3a5('INVOKE_DEFAULT', )
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Rig_Tune_Up_Be9A4(bpy.types.Operator):
    bl_idname = "sna.rig_tune_up_be9a4"
    bl_label = "Rig Tune Up"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.context.scene.sna_rig_tuning_menu.preview_selection = 'Select All'
        for i_3F3B0 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1])):
            sna_set_weight_4C3C1(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb)
            for i_C7B44 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles)):
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].rig_tuning_group.suspension_stiffness = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].rig_tuning_group.suspension_stiffness
                sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].rig_tuning_group.suspension_damping = sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].rig_tuning_group.suspension_damping
                for i_B77C2 in range(len(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].axle_wheels)):
                    sna_set_weight_4C3C1(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].axle_wheels[i_B77C2].wheel_rb)
                    sna_set_wheel_constraint_0F00E(sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].axle_wheels[i_B77C2].wheel_rb, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.sna_body_axles[i_C7B44].axle_wheels[i_B77C2].wheel_constraint, sna_get_rig_bodywheel_list_188BE(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig])[1][i_3F3B0].body_rb.rigid_body.mass)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Snap_To_Ground_F6C01(bpy.types.Operator):
    bl_idname = "sna.snap_to_ground_f6c01"
    bl_label = "Snap to Ground"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        if (bpy.context.scene.sna_rbc_scene_.ground != None):
            bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location = (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location[0], bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_control_obj.location[1], bpy.context.scene.sna_rbc_scene_.ground.location[2])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


class SNA_OT_Is_Empty_46D86(bpy.types.Operator):
    bl_idname = "sna.is_empty_46d86"
    bl_label = "Is Empty"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        bpy.context.view_layer.objects.active.select_set(state=False, )
        for i_4AE4D in range(len(bpy.context.view_layer.objects.active.children)):
            bpy.context.view_layer.objects.active.children[i_4AE4D].select_set(state=True, )
        import bmesh
        import mathutils
        # from blender templates

        def add_box(width, height, depth):
            """
            This function takes inputs and returns vertex and face arrays.
            no actual mesh data creation is done here.
            """
            verts = [(+1.0, +1.0, -1.0),
                     (+1.0, -1.0, -1.0),
                     (-1.0, -1.0, -1.0),
                     (-1.0, +1.0, -1.0),
                     (+1.0, +1.0, +1.0),
                     (+1.0, -1.0, +1.0),
                     (-1.0, -1.0, +1.0),
                     (-1.0, +1.0, +1.0),
                     ]
            faces = [(0, 1, 2, 3),
                     (4, 7, 6, 5),
                     (0, 4, 5, 1),
                     (1, 5, 6, 2),
                     (2, 6, 7, 3),
                     (4, 0, 3, 7),
                    ]
            # apply size
            for i, v in enumerate(verts):
                verts[i] = v[0] * width, v[1] * depth, v[2] * height
            return verts, faces

        def group_bounding_box():
            minx, miny, minz = (999999.0,)*3
            maxx, maxy, maxz = (-999999.0,)*3
            location = [0.0,]*3
            for obj in bpy.context.selected_objects:
                for v in obj.bound_box:
                    v_world = obj.matrix_world @ mathutils.Vector((v[0],v[1],v[2]))
                    if v_world[0] < minx:
                        minx = v_world[0]
                    if v_world[0] > maxx:
                        maxx = v_world[0]
                    if v_world[1] < miny:
                        miny = v_world[1]
                    if v_world[1] > maxy:
                        maxy = v_world[1]
                    if v_world[2] < minz:
                        minz = v_world[2]
                    if v_world[2] > maxz:
                        maxz = v_world[2]
            verts_loc, faces = add_box((maxx-minx)/2, (maxz-minz)/2, (maxy-miny)/2)
            mesh = bpy.data.meshes.new("BoundingBox")
            bm = bmesh.new()
            for v_co in verts_loc:
                bm.verts.new(v_co)
            bm.verts.ensure_lookup_table()
            for f_idx in faces:
                bm.faces.new([bm.verts[i] for i in f_idx])
            bm.to_mesh(mesh)
            mesh.update()
            location[0] = minx+((maxx-minx)/2)
            location[1] = miny+((maxy-miny)/2)
            location[2] = minz+((maxz-minz)/2)
            bbox = object_utils.object_data_add(bpy.context, mesh, operator=None)
            # does a bounding box need to display more than the bounds??
            bbox.location = location
            bbox.display_type = 'BOUNDS'
            bbox.hide_render = True
        group_bounding_box()
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_create_empty_collection_20DB3():
    collection_E2221 = bpy.data.collections.new(name='EmptSubColl', )
    bpy.context.scene.collection.children.link(child=collection_E2221, )
    return collection_E2221


def sna_obj_convex_hull_85CAF(Model_OBJ, Car_body):
    collection_0_f8502 = sna_create_empty_collection_20DB3()
    if Model_OBJ.type == 'EMPTY':
        for i_98B10 in range(len(Model_OBJ.children)):
            collection_0_f8502.objects.link(object=Model_OBJ.children[i_98B10], )
    else:
        collection_0_f8502.objects.link(object=Model_OBJ, )
        if (len(Model_OBJ.children) == 0):
            pass
        else:
            for i_34F30 in range(len(Model_OBJ.children)):
                collection_0_f8502.objects.link(object=Model_OBJ.children[i_34F30], )
    sna_collection_convex_hull_33_DD64F(collection_0_f8502, Car_body)
    bpy.data.collections.remove(collection=collection_0_f8502, )


def sna_reset_carrb_mesh_23CA0():
    bpy.ops.object.select_all('INVOKE_DEFAULT', action='DESELECT')
    for i_0AECB in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
        bpy.context.view_layer.objects.active = bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_0AECB].body_rb
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
        bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
        bpy.ops.mesh.delete('INVOKE_DEFAULT', type='VERT')
        bpy.ops.mesh.primitive_cube_add('INVOKE_DEFAULT', size=2.0, location=(0.0, 0.0, 0.0))
        bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')


class SNA_OT_Create_Convex_Hull_78B8A(bpy.types.Operator):
    bl_idname = "sna.create_convex_hull_78b8a"
    bl_label = "Create Convex Hull"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_E29BC in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
            if (bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E29BC].body_collection == None):
                sna_obj_convex_hull_85CAF(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E29BC].body_model, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E29BC].body_rb)
            else:
                sna_collection_convex_hull_33_DD64F(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E29BC].body_collection, bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_E29BC].body_rb)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_set_weight_position_func_34188(Body_Prop):
    Body_Prop.physics_weight_position_button = True
    Body_Prop.body_rb.location = (Body_Prop.body_rb.location[0], Body_Prop.body_rb.location[1], float(Body_Prop.body_rb.location[2] - float(Body_Prop.body_rb.dimensions[2] / 2.0)))
    Body_Prop.physics_weight_position_button = False


class SNA_OT_Set_Weight_Position__74A84(bpy.types.Operator):
    bl_idname = "sna.set_weight_position__74a84"
    bl_label = "Set Weight Position "
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and False:
            cls.poll_message_set()
        return not False

    def execute(self, context):
        for i_15FDC in range(len(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies)):
            sna_set_weight_position_func_34188(bpy.context.scene.sna_rbc_rig_collection[bpy.context.scene.sna_active_rig].rig_bodies[i_15FDC])
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)


def sna_collection_convex_hull_33_DD64F(Collection, Car_Body):
    sna_hide_obj_select_71598(Car_Body, False, False, False, False)
    modifier_5CB67 = Car_Body.modifiers.new(name='RBC Geo Nodes', type='NODES', )
    if property_exists("bpy.data.node_groups['RBC Collection Nodes']", globals(), locals()):
        pass
    else:
        before_data = list(bpy.data.node_groups)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'RBC Assets.blend') + r'\NodeTree', filename='RBC Collection Nodes', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.node_groups)))
        appended_19833 = None if not new_data else new_data[0]
    modifier_5CB67.node_group = bpy.data.node_groups['RBC Collection Nodes']
    modifier_5CB67['Input_0'] = Collection
    modifier_38302 = Car_Body.modifiers.new(name='CollectionNodes', type='WELD', )
    modifier_38302.merge_threshold = 0.05000000074505806
    bpy.context.view_layer.objects.active = Car_Body
    bpy.context.view_layer.objects.active.select_set(state=True, )
    bpy.ops.object.convert('INVOKE_DEFAULT', target='MESH')
    group_A5044 = bpy.context.view_layer.objects.active.vertex_groups.new(name='RBC Group', )
    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='EDIT')
    bpy.ops.mesh.select_all('INVOKE_DEFAULT', action='SELECT')
    bpy.ops.object.vertex_group_assign('INVOKE_DEFAULT', )
    bpy.ops.object.mode_set('INVOKE_DEFAULT', mode='OBJECT')
    bpy.context.object.data.materials.clear()
    bpy.context.view_layer.objects.active.select_set(state=False, )
    sna_hide_obj_select_71598(Car_Body, True, False, False, False)


@persistent
def frame_change_post_handler_73628(dummy):
    pass


class SNA_PT_RIGID_BODY_SETTINGS_45887(bpy.types.Panel):
    bl_label = 'Rigid Body Settings'
    bl_idname = 'SNA_PT_RIGID_BODY_SETTINGS_45887'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_RBC_COLLISIONS_3D783'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not ((not property_exists("bpy.context.view_layer.objects.active.rigid_body.enabled", globals(), locals())))

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        if property_exists("bpy.context.view_layer.objects.active.rigid_body.enabled", globals(), locals()):
            grid_01327 = layout.grid_flow(columns=1, row_major=False, even_columns=False, even_rows=False, align=False)
            grid_01327.enabled = True
            grid_01327.active = True
            grid_01327.use_property_split = False
            grid_01327.use_property_decorate = False
            grid_01327.alignment = 'Expand'.upper()
            grid_01327.scale_x = 1.0
            grid_01327.scale_y = 1.0
            if not True: grid_01327.operator_context = "EXEC_DEFAULT"
            if hasattr(bpy.types,"PHYSICS_PT_rigid_body"):
                if not hasattr(bpy.types.PHYSICS_PT_rigid_body, "poll") or bpy.types.PHYSICS_PT_rigid_body.poll(context):
                    bpy.types.PHYSICS_PT_rigid_body.draw(self, context)
                else:
                    grid_01327.label(text="Can't display this panel here!", icon="ERROR")
            else:
                grid_01327.label(text="Can't display this panel!", icon="ERROR")
            if hasattr(bpy.types,"PHYSICS_PT_rigid_body_settings"):
                if not hasattr(bpy.types.PHYSICS_PT_rigid_body_settings, "poll") or bpy.types.PHYSICS_PT_rigid_body_settings.poll(context):
                    bpy.types.PHYSICS_PT_rigid_body_settings.draw(self, context)
                else:
                    grid_01327.label(text="Can't display this panel here!", icon="ERROR")
            else:
                grid_01327.label(text="Can't display this panel!", icon="ERROR")
            if hasattr(bpy.types,"PHYSICS_PT_rigid_body_collisions"):
                if not hasattr(bpy.types.PHYSICS_PT_rigid_body_collisions, "poll") or bpy.types.PHYSICS_PT_rigid_body_collisions.poll(context):
                    bpy.types.PHYSICS_PT_rigid_body_collisions.draw(self, context)
                else:
                    grid_01327.label(text="Can't display this panel here!", icon="ERROR")
            else:
                grid_01327.label(text="Can't display this panel!", icon="ERROR")
            if hasattr(bpy.types,"PHYSICS_PT_rigid_body_collisions_surface"):
                if not hasattr(bpy.types.PHYSICS_PT_rigid_body_collisions_surface, "poll") or bpy.types.PHYSICS_PT_rigid_body_collisions_surface.poll(context):
                    bpy.types.PHYSICS_PT_rigid_body_collisions_surface.draw(self, context)
                else:
                    grid_01327.label(text="Can't display this panel here!", icon="ERROR")
            else:
                grid_01327.label(text="Can't display this panel!", icon="ERROR")


class SNA_PT_PERFORMANCE_74559(bpy.types.Panel):
    bl_label = 'Performance'
    bl_idname = 'SNA_PT_PERFORMANCE_74559'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = ''
    bl_order = 0
    bl_parent_id = 'SNA_PT_RBC_COLLECTION_8ECBE'
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (True)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        col_00C5F = layout.column(heading='Performance', align=False)
        col_00C5F.alert = False
        col_00C5F.enabled = True
        col_00C5F.active = True
        col_00C5F.use_property_split = False
        col_00C5F.use_property_decorate = False
        col_00C5F.scale_x = 1.0
        col_00C5F.scale_y = 1.0
        col_00C5F.alignment = 'Expand'.upper()
        col_00C5F.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        col_00C5F.prop(bpy.context.scene.sna_rbc_scene_, 'performance', text='', icon_value=0, emboss=True)
        col_00C5F.prop(bpy.context.scene.rigidbody_world, 'use_split_impulse', text='Split Impulse', icon_value=0, emboss=True)
        col_00C5F.prop(bpy.context.scene.rigidbody_world, 'substeps_per_frame', text='Substeps Per Frame', icon_value=0, emboss=True)
        col_00C5F.prop(bpy.context.scene.rigidbody_world, 'solver_iterations', text='Solver Iterations', icon_value=0, emboss=True)


class SNA_GROUP_sna_rbc_setup_advanced_group(bpy.types.PropertyGroup):
    show_collections: bpy.props.BoolProperty(name='Show Collections', description='Use collections to set up rig', options={'HIDDEN'}, default=False)
    show_add_button: bpy.props.BoolProperty(name='Show ADD Button', description='Add extra objects like brake calipers', options={'HIDDEN'}, default=False)
    show_customize: bpy.props.BoolProperty(name='Show Customize', description='', default=False)
    show_advanced: bpy.props.BoolProperty(name='Show Advanced', description='Shows advanced featues like Axle Types', options={'HIDDEN'}, default=False)


class SNA_GROUP_sna_rbc_objs(bpy.types.PropertyGroup):
    obj: bpy.props.PointerProperty(name='OBJ', description='', type=bpy.types.Object)


class SNA_GROUP_sna_rbc_wheel_group(bpy.types.PropertyGroup):
    wheel_rb: bpy.props.PointerProperty(name='Wheel RB', description='', type=bpy.types.Object)
    wheel_constraint: bpy.props.PointerProperty(name='Wheel Constraint', description='', type=bpy.types.Object)
    wheel_steeringmotor: bpy.props.PointerProperty(name='Wheel SteeringMotor', description='', type=bpy.types.Object)
    wheel_motor: bpy.props.PointerProperty(name='Wheel Motor', description='', type=bpy.types.Object)
    wheel_extra: bpy.props.PointerProperty(name='Wheel Extra', description='', type=bpy.types.Object)
    wheel_animobj: bpy.props.PointerProperty(name='Wheel AnimObj', description='', type=bpy.types.Object)
    wheel_button: bpy.props.BoolProperty(name='Wheel Button', description='', options={'HIDDEN'}, default=False, update=sna_update_wheel_button_CA318)
    wheel_extra_button: bpy.props.BoolProperty(name='Wheel Extra Button', description='', options={'HIDDEN'}, default=False, update=sna_update_wheel_extra_button_926C2)
    wheel_model: bpy.props.PointerProperty(name='Wheel Model', description='', type=bpy.types.Object)
    wheel_collection: bpy.props.PointerProperty(name='Wheel Collection', description='', type=bpy.types.Collection, update=sna_update_wheel_collection_AF401)
    wheel_type: bpy.props.EnumProperty(name='Wheel Type', description='', items=[('Drive', 'Drive', '', 0, 0), ('Steering', 'Steering', '', 0, 1), ('Drive/Steering', 'Drive/Steering', '', 0, 2), ('Dead', 'Dead', '', 0, 3)])
    wheel_boundingbox: bpy.props.PointerProperty(name='Wheel BoundingBox', description='', type=bpy.types.Object)
    wheel_cambertilt_obj: bpy.props.PointerProperty(name='Wheel CamberTilt Obj', description='', type=bpy.types.Object)
    wheel_brakecaliper_obj: bpy.props.PointerProperty(name='Wheel BrakeCaliper Obj', description='', type=bpy.types.Object)


class SNA_GROUP_sna_rbc_body_group(bpy.types.PropertyGroup):
    body_button: bpy.props.BoolProperty(name='Body Button', description='', options={'HIDDEN'}, default=False, update=sna_update_body_button_846FC)
    body_rb: bpy.props.PointerProperty(name='Body RB', description='', type=bpy.types.Object)
    body_collection: bpy.props.PointerProperty(name='Body Collection', description='', type=bpy.types.Collection, update=sna_update_body_collection_FC79B)
    body_model: bpy.props.PointerProperty(name='Body Model', description='', type=bpy.types.Object)
    body_hitch_obj: bpy.props.PointerProperty(name='Body Hitch OBJ', description='', type=bpy.types.Object)
    body_hitch_button: bpy.props.BoolProperty(name='Body Hitch Button', description='Enables Hitch to move to desired postion', options={'HIDDEN'}, default=False, update=sna_update_body_hitch_button_51522)
    body_tuning_button: bpy.props.BoolProperty(name='Body Tuning Button', description='', options={'HIDDEN'}, default=False, update=sna_update_body_tuning_button_21E68)
    physics_weight: bpy.props.FloatProperty(name='Physics: Weight', description='', default=1.0, subtype='NONE', unit='NONE', min=0.009999999776482582, soft_min=0.009999999776482582, max=1000.0, soft_max=10000.0, step=3, precision=2, update=sna_update_physics_weight_E6ACC)
    physics_weight_position_button: bpy.props.BoolProperty(name='Physics: Weight Position Button', description='', default=False, update=sna_update_physics_weight_position_button_115B6)
    physics_roll_constraint: bpy.props.PointerProperty(name='Physics: Roll Constraint', description='', type=bpy.types.Object)
    physics_roll_constraint_x_angle: bpy.props.FloatProperty(name='Physics: Roll Constraint X angle', description='', default=0.7852500081062317, subtype='ANGLE', unit='NONE', min=0.0, max=1.5705000162124634, step=3, precision=1, update=sna_update_physics_roll_constraint_x_angle_F95D6)
    physics_roll_constraint_y_angle: bpy.props.FloatProperty(name='Physics: Roll Constraint Y angle', description='', default=0.7852500081062317, subtype='ANGLE', unit='NONE', min=0.0, max=1.5705000162124634, step=3, precision=1, update=sna_update_physics_roll_constraint_y_angle_27A57)
    physics_roll_constraint_button: bpy.props.BoolProperty(name='Physics: Roll Constraint Button', description='', default=False, update=sna_update_physics_roll_constraint_button_C7BCE)
    physics_lean_constraint: bpy.props.PointerProperty(name='Physics: Lean Constraint', description='', type=bpy.types.Object)
    physics_lean_strength: bpy.props.FloatProperty(name='Physics: Lean Strength', description='', default=10.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)
    body_boundingbox: bpy.props.PointerProperty(name='Body BoundingBox', description='', type=bpy.types.Object)
    body_anim_obj: bpy.props.PointerProperty(name='Body Anim Obj', description='', type=bpy.types.Object)


class SNA_GROUP_sna_set_up_preview_group(bpy.types.PropertyGroup):
    vehicle_body_button: bpy.props.BoolVectorProperty(name='Vehicle Body Button', description='', options={'HIDDEN'}, size=3, default=(False, False, False))
    vehicle_is_double: bpy.props.BoolProperty(name='Vehicle is Double', description='', default=False)
    int: bpy.props.IntVectorProperty(name='Int', description='', size=3, default=(0, 0, 0), subtype='NONE', min=1, max=10)
    new_property: bpy.props.StringProperty(name='New Property', description='', default='', subtype='NONE', maxlen=0)


class SNA_GROUP_sna_vehicle_preview_propeties(bpy.types.PropertyGroup):
    vehicle_body: bpy.props.BoolProperty(name='Vehicle Body', description='', default=False)
    vehicle_body_axles: bpy.props.IntProperty(name='Vehicle Body Axles', description='', default=0, subtype='NONE')
    vehicle_bed: bpy.props.StringProperty(name='Vehicle Bed', description='', default='', subtype='NONE', maxlen=0)
    vehicle_bed_axles: bpy.props.IntProperty(name='Vehicle Bed Axles', description='', default=0, subtype='NONE')
    axle_type: bpy.props.EnumProperty(name='Axle Type', description='', items=[('1', '1', '', 0, 0), ('2', '2', '', 0, 1)])
    vehicle_trailer: bpy.props.BoolProperty(name='Vehicle Trailer', description='', default=False)
    vehicle_trailer_axles: bpy.props.IntProperty(name='Vehicle Trailer Axles', description='', default=0, subtype='NONE')


class SNA_GROUP_sna_custom_vehicle_properties(bpy.types.PropertyGroup):
    vehicle_front_axle_wheels: bpy.props.IntProperty(name='Vehicle Front Axle Wheels', description='', default=2, subtype='NONE', min=1, max=2)
    vehicle_bed: bpy.props.BoolProperty(name='Vehicle Bed', description='', default=False)
    vehicle_back_axle_wheels: bpy.props.IntProperty(name='Vehicle Back Axle Wheels', description='', default=2, subtype='NONE', min=1, max=2)
    extra_back_axles: bpy.props.IntProperty(name='Extra Back Axles', description='', default=0, subtype='NONE', min=0, max=10)
    extra_back_axles_wheels: bpy.props.IntProperty(name='Extra Back Axles Wheels', description='', default=2, subtype='NONE', min=1, max=2)
    vehicle_trailer: bpy.props.IntProperty(name='Vehicle Trailer', description='', default=0, subtype='NONE', min=0, max=1)
    vehicle_trailer_axles: bpy.props.IntProperty(name='Vehicle Trailer Axles', description='', default=2, subtype='NONE', min=1, max=10)
    preview_button: bpy.props.BoolProperty(name='Preview Button', description='', options={'HIDDEN'}, default=False)
    enable_preview: bpy.props.BoolProperty(name='Enable Preview', description='', options={'HIDDEN'}, default=False)
    enable_menu: bpy.props.BoolProperty(name='Enable Menu', description='', options={'HIDDEN'}, default=False)


class SNA_GROUP_sna_rig_drivers_group(bpy.types.PropertyGroup):
    steering: bpy.props.FloatProperty(name='Steering', description='Vehicle Steering: Negative value steers left positive value steers right', default=0.0, subtype='NONE', unit='NONE', min=-1.0, max=1.0, step=1, precision=1)
    steering_power: bpy.props.FloatProperty(name='Steering Power', description='Increases steering response', default=15.0, subtype='NONE', unit='NONE', min=0.0, max=100.0, soft_max=1000.0, step=1, precision=0)
    drive: bpy.props.FloatProperty(name='Drive', description='', default=0.0, subtype='UNSIGNED', unit='VELOCITY', min=-1000.0, max=1000.0, step=3, precision=2)
    torque: bpy.props.FloatProperty(name='Torque', description='Increases Wheel Torque', default=1.0, subtype='NONE', unit='NONE', min=0.10000000149011612, max=100.0, soft_max=1000.0, step=3, precision=2)
    brake: bpy.props.BoolProperty(name='Brake', description=' Vehicle Brakes', default=False)
    brake_strength: bpy.props.FloatProperty(name='Brake Strength', description='Increases Brake response', default=10.0, subtype='NONE', unit='NONE', min=0.0, max=100.0, soft_max=1000.0, step=3, precision=0)
    disable_drive: bpy.props.BoolProperty(name='Disable Drive', description='', default=False, update=sna_update_disable_drive_D2572)
    disable_steering: bpy.props.BoolProperty(name='Disable Steering', description='', default=False, update=sna_update_disable_steering_7C4F0)
    time: bpy.props.FloatProperty(name='Time', description='Seconds to reach Target Speed', default=0.0, subtype='TIME', unit='TIME', min=0.0, max=120.0, soft_max=1000.0, step=3, precision=2)
    target_speed: bpy.props.FloatProperty(name='Target Speed', description='Target Speed of Vehicle', default=0.0, subtype='NONE', unit='NONE', min=-420.0, soft_min=-100.0, max=420.0, soft_max=1000.0, step=3, precision=0)
    first_frame: bpy.props.IntProperty(name='First Frame', description='', default=0, subtype='NONE')
    acceleration: bpy.props.FloatProperty(name='Acceleration', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    current_speed: bpy.props.FloatProperty(name='Current Speed', description='a', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    length: bpy.props.FloatProperty(name='Length', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)


class SNA_GROUP_sna_rig_tuning_group(bpy.types.PropertyGroup):
    show_pivot_points: bpy.props.BoolProperty(name='Show Pivot Points', description='', default=False, update=sna_update_show_pivot_points_3B8A1)
    show_turn_radius: bpy.props.BoolProperty(name='Show Turn Radius', description='', default=False)
    wheels_pivot_points: bpy.props.FloatProperty(name='Wheels: Pivot Points', description='Point at which wheel rotates around', default=0.0, subtype='NONE', unit='NONE', step=3, precision=2, update=sna_update_wheels_pivot_points_AFAE3)
    wheels_camber_angle: bpy.props.FloatProperty(name='Wheels: Camber Angle', description='The angle between the vertical axis of a wheel and the vertical axis of the vehicle', default=0.0, subtype='ANGLE', unit='ROTATION', min=-1.5707000494003296, max=1.5707000494003296, step=6, precision=1, update=sna_update_wheels_camber_angle_DE85F)
    wheels_turn_radius: bpy.props.FloatProperty(name='Wheels: Turn Radius', description='The angle limit of how much a wheel can rotate when steering', default=0.6108649969100952, subtype='ANGLE', unit='ROTATION', min=0.0, max=1.5707000494003296, step=6, precision=1, update=sna_update_wheels_turn_radius_57316)
    suspension_limits: bpy.props.FloatProperty(name='Suspension: Limits', description='Limit length of suspension', default=1.0, subtype='NONE', unit='NONE', min=0.0, max=1.0, step=3, precision=2, update=sna_update_suspension_limits_19909)
    suspension_stiffness: bpy.props.FloatProperty(name='Suspension: Stiffness', description='Stiffness of suspension', default=50.0, subtype='NONE', unit='NONE', min=0.0, step=10, precision=2, update=sna_update_suspension_stiffness_5FF25)
    suspension_damping: bpy.props.FloatProperty(name='Suspension: Damping', description='Damning of stiffness(basicly dampens how bouncy the suspension is)', default=2.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2, update=sna_update_suspension_damping_1BB2D)
    physics_tire_friction: bpy.props.FloatProperty(name='Physics: Tire Friction', description='Friction of Tires(Idk what to tell ya)', default=5.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2, update=sna_update_physics_tire_friction_E904C)
    physics_weight: bpy.props.FloatProperty(name='Physics: Weight', description='Weight of the Vechicle', default=0.0, subtype='NONE', unit='NONE', min=1.0, max=10.0, step=3, precision=2, update=sna_update_physics_weight_E6ACC)


class SNA_GROUP_sna_rig_tuning_menu_group(bpy.types.PropertyGroup):
    preview_selection: bpy.props.EnumProperty(name='Preview Selection', description='', options={'HIDDEN'}, items=[('Select All', 'Select All', 'Allows for selection of all tunable vehicle parts', 0, 0), ('Individual', 'Individual', 'Allows for selection of individual tunable vehicle parts', 0, 1)], update=sna_update_preview_selection_0853C)
    show_pivot_points: bpy.props.BoolProperty(name='Show Pivot Points', description='', default=False, update=sna_update_show_pivot_points_3B8A1)
    show_turn_radius: bpy.props.BoolProperty(name='Show Turn Radius', description='', default=False)
    minimize_preview: bpy.props.BoolProperty(name='Minimize Preview', description='', options={'HIDDEN'}, default=False)
    axlebody: bpy.props.EnumProperty(name='Axle/Body', description='', items=[('Axle', 'Axle', '', 0, 0), ('Body', 'Body', '', 0, 1)])
    drive_type: bpy.props.EnumProperty(name='Drive Type', description='', items=[('2WD', '2WD', '2 Wheel Drive', 0, 0), ('4WD', '4WD', '4 Wheel Drive', 0, 1), ('FWD', 'FWD', 'Front Wheel Drive', 0, 2), ('DSD', 'DSD', 'Differential Steering', 0, 3), ('RWS', 'RWS', 'Rear Wheel Steering', 0, 4), ('FWS+RWS', 'FWS+RWS', 'Front Wheels Steering and Rear Wheel Steering', 0, 5)], update=sna_update_drive_type_7DA4C)


class SNA_GROUP_sna_rbc_control_menu_group(bpy.types.PropertyGroup):
    worldspeed: bpy.props.FloatProperty(name='WorldSpeed', description='Controls speed of Rigid Body World simulation', default=0.5, subtype='NONE', unit='NONE', min=0.0, max=2.0, step=3, precision=1)
    carspeed: bpy.props.FloatProperty(name='CarSpeed', description='Controls top speed of vehicle', default=20.0, subtype='NONE', unit='NONE', min=-1000.0, max=1000.0, step=3, precision=2)
    cntrl_xbox_running: bpy.props.BoolProperty(name='CNTRL_Xbox Running', description='', default=False)
    cntrl_keyboard_running: bpy.props.BoolProperty(name='CNTRL_Keyboard Running', description='', default=False)
    controller_maps: bpy.props.BoolProperty(name='Controller Maps', description='Shows Controls', default=False)
    disable_drive: bpy.props.BoolProperty(name='Disable Drive', description='', default=False, update=sna_update_disable_drive_D2572)
    disable_steering: bpy.props.BoolProperty(name='Disable Steering', description='', default=False, update=sna_update_disable_steering_7C4F0)
    advanced_controls: bpy.props.BoolProperty(name='Advanced Controls', description='', default=False)
    w_key_down: bpy.props.BoolProperty(name='W Key Down', description='', default=False)
    s_key_down: bpy.props.BoolProperty(name='S Key Down', description='', default=False)
    a_key_down: bpy.props.BoolProperty(name='A Key Down', description='', default=False)
    d_key_down: bpy.props.BoolProperty(name='D Key Down', description='', default=False)


class SNA_GROUP_sna_rig_tuning_all_group(bpy.types.PropertyGroup):
    physics_tire_friction: bpy.props.FloatProperty(name='Physics: Tire Friction', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6, update=sna_update_physics_tire_friction_E904C)


class SNA_GROUP_sna_animation_menu_group(bpy.types.PropertyGroup):
    enable_anim_constraint: bpy.props.BoolProperty(name='Enable Anim Constraint', description='', default=False, update=sna_update_enable_anim_constraint_71574)
    enable_kinematic_: bpy.props.BoolProperty(name='Enable Kinematic ', description='', default=False)
    enable_breakable: bpy.props.BoolProperty(name='Enable Breakable', description='', default=False, update=sna_update_enable_breakable_35B13)
    breakable_threshold: bpy.props.FloatProperty(name='Breakable Threshold', description='', default=10.0, subtype='NONE', unit='NONE', step=3, precision=2, update=sna_update_breakable_threshold_37669)
    record_keyframes: bpy.props.BoolProperty(name='Record Keyframes', description='', default=False, update=sna_update_record_keyframes_1615C)
    rig_keyframes_baked: bpy.props.BoolProperty(name='Rig Keyframes Baked', description='', default=False)


class SNA_GROUP_sna_rig_guides_group(bpy.types.PropertyGroup):
    enable_guide: bpy.props.BoolProperty(name='Enable Guide', description='Enables Guiding Function', default=False, update=sna_update_enable_guide_918E0)
    guide_object: bpy.props.PointerProperty(name='Guide Object', description='', type=bpy.types.Object)
    guide_path: bpy.props.PointerProperty(name='Guide Path', description='', type=bpy.types.Object)
    top_speed: bpy.props.FloatProperty(name='Top Speed', description='', default=100.0, subtype='NONE', unit='NONE', min=0.0, step=3, precision=2)
    auto_drive: bpy.props.BoolProperty(name='Auto Drive', description='Enables Auto Drive Function', default=False)
    auto_reverse: bpy.props.BoolProperty(name='Auto Reverse', description='Enables Auto Reverse Function', default=False)
    auto_brake: bpy.props.BoolProperty(name='Auto Brake', description='Enables Auto Brake Function', default=False)
    distance: bpy.props.FloatProperty(name='Distance', description='Distance Between Guide Object and Vehicle Before Braking', default=1.0, subtype='NONE', unit='NONE', min=0.10000000149011612, max=100.0, step=3, precision=2)
    reverse_angle: bpy.props.FloatProperty(name='Reverse Angle', description='Angle at which vehicle will reverse.', default=0.785398006439209, subtype='ANGLE', unit='NONE', min=0.0, max=3.141592025756836, step=3, precision=1)
    length: bpy.props.FloatProperty(name='Length', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    min_speed: bpy.props.FloatProperty(name='Min Speed', description='Minimum Speed', default=0.0, subtype='NONE', unit='NONE', step=3, precision=1)
    max_speed: bpy.props.FloatProperty(name='Max Speed', description='Maximum Speed', default=60.0, subtype='NONE', unit='NONE', step=3, precision=1)
    guide_path_distance: bpy.props.FloatProperty(name='Guide Path Distance', description='Extends distance between Vehicle and Guide Object', default=5.0, subtype='NONE', unit='NONE', min=1.0, max=10.0, step=3, precision=2)


class SNA_GROUP_sna_speedometer_group(bpy.types.PropertyGroup):
    mph: bpy.props.StringProperty(name='MPH', description='', default='', subtype='NONE', maxlen=0)
    kmh: bpy.props.StringProperty(name='Km/h', description='', default='', subtype='NONE', maxlen=0)
    run_speedometer: bpy.props.BoolProperty(name='Run Speedometer', description='', default=False)
    speedometer_unit: bpy.props.EnumProperty(name='Speedometer Unit', description='', options={'HIDDEN'}, items=[('MPH', 'MPH', 'Show MPH', 0, 0), ('Km/h', 'Km/h', 'Show Km/h', 0, 1)])
    speedometer_loc: bpy.props.FloatVectorProperty(name='Speedometer Loc', description='', size=2, default=(10.0, -180.0), subtype='NONE', unit='NONE', step=10, precision=2)
    speedometer_size: bpy.props.IntProperty(name='Speedometer Size', description='', default=72, subtype='NONE')
    speed_value: bpy.props.FloatProperty(name='Speed Value', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=1)


class SNA_GROUP_sna_rbc_scene_group(bpy.types.PropertyGroup):
    performance: bpy.props.EnumProperty(name='Performance', description='', options={'HIDDEN'}, items=[('Low', 'Low', '', 0, 0), ('Medium', 'Medium', '', 0, 1), ('High', 'High', '', 0, 2)], update=sna_update_performance_9CF7A)
    ground: bpy.props.PointerProperty(name='Ground', description='', type=bpy.types.Object)
    follow_camera: bpy.props.PointerProperty(name='Follow Camera', description='', type=bpy.types.Object)
    chase_camera: bpy.props.PointerProperty(name='Chase Camera', description='', type=bpy.types.Object)


class SNA_GROUP_sna_rbc_rig_group(bpy.types.PropertyGroup):
    rig_control_obj: bpy.props.PointerProperty(name='Rig Control Obj', description='', type=bpy.types.Object)
    rig_obj_collection: bpy.props.CollectionProperty(name='Rig Obj Collection', description='', type=SNA_GROUP_sna_rbc_objs)
    rig_wheels_collection: bpy.props.CollectionProperty(name='Rig Wheels Collection', description='', type=SNA_GROUP_sna_rbc_wheel_group)
    rig_model_collection: bpy.props.CollectionProperty(name='Rig Model Collection', description='', type=SNA_GROUP_sna_rbc_objs)
    rig_collection: bpy.props.PointerProperty(name='Rig Collection', description='', type=bpy.types.Collection)
    rig_rigged: bpy.props.BoolProperty(name='Rig Rigged', description='', default=False)
    rig_type: bpy.props.EnumProperty(name='Rig Type', description='', items=sna_rbc_rig_group_rig_type_enum_items)
    rig_bodies: bpy.props.CollectionProperty(name='Rig Bodies', description='', type=SNA_GROUP_sna_rbc_body_group)
    rig_name: bpy.props.StringProperty(name='Rig Name', description='', default='', subtype='NONE', maxlen=0, update=sna_update_rig_name_080C1)
    rig_drivers: bpy.props.PointerProperty(name='Rig Drivers', description='', type=SNA_GROUP_sna_rig_drivers_group)
    rig_tuning_settings: bpy.props.PointerProperty(name='Rig Tuning Settings', description='', type=SNA_GROUP_sna_rig_tuning_group)
    drive_type: bpy.props.EnumProperty(name='Drive Type', description='', items=[('2WD', '2WD', '2 Wheel Drive', 0, 0), ('4WD', '4WD', '4 Wheel Drive', 0, 1), ('FWD', 'FWD', 'Front Wheel Drive', 0, 2), ('DSD', 'DSD', 'Differential Steering', 0, 3), ('RWS', 'RWS', 'Rear Wheel Steering', 0, 4), ('FWS+RWS', 'FWS+RWS', 'Front and Rear Wheel Steering', 0, 5)], update=sna_update_drive_type_7DA4C)
    rig_anim_objs: bpy.props.CollectionProperty(name='Rig Anim Objs', description='', type=SNA_GROUP_sna_rbc_objs)
    rig_animation: bpy.props.PointerProperty(name='Rig Animation', description='', type=SNA_GROUP_sna_animation_menu_group)
    rig_guide_control: bpy.props.PointerProperty(name='Rig Guide Control', description='', type=SNA_GROUP_sna_rig_guides_group)
    rig_asset_collection: bpy.props.BoolProperty(name='Rig Asset Collection', description='', default=False)
    hide_rig: bpy.props.BoolProperty(name='Hide Rig', description='Hide RBC Rig', default=False, update=sna_update_hide_rig_1C4DE)


class SNA_GROUP_sna_rbc_axle_group(bpy.types.PropertyGroup):
    axle_wheels: bpy.props.CollectionProperty(name='Axle Wheels', description='', type=SNA_GROUP_sna_rbc_wheel_group)
    axle_type: bpy.props.EnumProperty(name='Axle type', description='', items=[('Drive', 'Drive', '', 0, 0), ('Steering', 'Steering', '', 0, 1), ('Drive + Steering', 'Drive + Steering', '', 0, 2), ('Dead', 'Dead', '', 0, 3), ('Differential Steering', 'Differential Steering', '', 0, 4)], update=sna_update_axle_type_3DB7C)
    axle_tuning_button: bpy.props.BoolProperty(name='Axle Tuning Button', description='', options={'HIDDEN'}, default=False, update=sna_update_axle_tuning_button_9E7A2)
    rig_tuning_group: bpy.props.PointerProperty(name='Rig Tuning Group', description='', type=SNA_GROUP_sna_rig_tuning_group)
    camber_tilt_obj: bpy.props.PointerProperty(name='Camber Tilt Obj', description='', type=bpy.types.Object)
    reverse_drive: bpy.props.BoolProperty(name='Reverse Drive', description='', default=False, update=sna_update_reverse_drive_BF189)
    reverse_steering: bpy.props.BoolProperty(name='Reverse Steering', description='', default=False, update=sna_update_reverse_steering_A063A)


def register():
    global _icons
    _icons = bpy.utils.previews.new()
    bpy.utils.register_class(SNA_GROUP_sna_rbc_setup_advanced_group)
    bpy.utils.register_class(SNA_GROUP_sna_rbc_objs)
    bpy.utils.register_class(SNA_GROUP_sna_rbc_wheel_group)
    bpy.utils.register_class(SNA_GROUP_sna_rbc_body_group)
    bpy.utils.register_class(SNA_GROUP_sna_set_up_preview_group)
    bpy.utils.register_class(SNA_GROUP_sna_vehicle_preview_propeties)
    bpy.utils.register_class(SNA_GROUP_sna_custom_vehicle_properties)
    bpy.utils.register_class(SNA_GROUP_sna_rig_drivers_group)
    bpy.utils.register_class(SNA_GROUP_sna_rig_tuning_group)
    bpy.utils.register_class(SNA_GROUP_sna_rig_tuning_menu_group)
    bpy.utils.register_class(SNA_GROUP_sna_rbc_control_menu_group)
    bpy.utils.register_class(SNA_GROUP_sna_rig_tuning_all_group)
    bpy.utils.register_class(SNA_GROUP_sna_animation_menu_group)
    bpy.utils.register_class(SNA_GROUP_sna_rig_guides_group)
    bpy.utils.register_class(SNA_GROUP_sna_speedometer_group)
    bpy.utils.register_class(SNA_GROUP_sna_rbc_scene_group)
    bpy.utils.register_class(SNA_GROUP_sna_rbc_rig_group)
    bpy.utils.register_class(SNA_GROUP_sna_rbc_axle_group)
    bpy.types.Scene.sna_rbc_rig_collection = bpy.props.CollectionProperty(name='RBC Rig Collection', description='', type=SNA_GROUP_sna_rbc_rig_group)
    bpy.types.Scene.sna_rbc_collection_list = bpy.props.EnumProperty(name='RBC Collection List', description='', options={'HIDDEN'}, items=sna_rbc_collection_list_enum_items, update=sna_update_sna_rbc_collection_list_7F28B)
    bpy.types.Scene.sna_rbc_rig_type_menu = bpy.props.EnumProperty(name='RBC Rig Type Menu', description='', items=sna_rbc_rig_type_menu_enum_items, update=sna_update_sna_rbc_rig_type_menu_D497D)
    bpy.types.Scene.sna_rbc_set_up_advanced = bpy.props.PointerProperty(name='RBC Set Up Advanced', description='', type=SNA_GROUP_sna_rbc_setup_advanced_group)
    bpy.types.Scene.sna_rbc_rig_panel = bpy.props.EnumProperty(name='RBC Rig Panel', description='', items=sna_rbc_rig_panel_enum_items, options={'ENUM_FLAG'}, update=sna_update_sna_rbc_rig_panel_F8101)
    bpy.types.Scene.sna_rbc_rig_panel_icon = bpy.props.EnumProperty(name='RBC Rig Panel Icon', description='', items=sna_rbc_rig_panel_icon_enum_items)
    bpy.types.Object.sna_body_axles = bpy.props.CollectionProperty(name='Body Axles', description='', type=SNA_GROUP_sna_rbc_axle_group)
    bpy.types.Object.sna_control_rig_car_bodies = bpy.props.CollectionProperty(name='Control Rig Car Bodies', description='', type=SNA_GROUP_sna_rbc_body_group)
    bpy.types.Scene.sna_set_up_preview = bpy.props.PointerProperty(name='Set Up Preview', description='', type=SNA_GROUP_sna_set_up_preview_group)
    bpy.types.Scene.sna_custom_vehicle_set = bpy.props.PointerProperty(name='Custom Vehicle Set', description='', type=SNA_GROUP_sna_custom_vehicle_properties)
    bpy.types.Scene.sna_rig_control_panel = bpy.props.EnumProperty(name='Rig Control Panel', description='', options={'HIDDEN'}, items=sna_rig_control_panel_enum_items, update=sna_update_sna_rig_control_panel_3F2AD)
    bpy.types.Scene.sna_rig_tuning_enum = bpy.props.EnumProperty(name='Rig Tuning Enum', description='', items=sna_rig_tuning_enum_enum_items, options={'ENUM_FLAG'})
    bpy.types.Scene.sna_rig_tuning_menu = bpy.props.PointerProperty(name='Rig Tuning Menu', description='', type=SNA_GROUP_sna_rig_tuning_menu_group)
    bpy.types.Object.sna_rig_control_drivers = bpy.props.PointerProperty(name='Rig Control Drivers', description='', type=SNA_GROUP_sna_rig_drivers_group)
    bpy.types.Scene.sna_active_rig = bpy.props.StringProperty(name='Active Rig', description='', default='', subtype='NONE', maxlen=0, update=sna_update_sna_active_rig_9D8DD)
    bpy.types.Scene.sna_rbc_ground_plane = bpy.props.PointerProperty(name='RBC Ground Plane', description='', type=bpy.types.Object, update=sna_update_sna_rbc_ground_plane_27EFD)
    bpy.types.Scene.sna_overlap_bool = bpy.props.BoolProperty(name='Overlap Bool', description='', default=False)
    bpy.types.Scene.sna_locdata = bpy.props.FloatVectorProperty(name='LocData', description='', size=3, default=(0.0, 0.0, 0.0), subtype='NONE', unit='NONE', step=3, precision=6)
    bpy.types.Object.sna_rotdata = bpy.props.FloatVectorProperty(name='RotData', description='', size=3, default=(0.0, 0.0, 0.0), subtype='NONE', unit='NONE', step=3, precision=6)
    bpy.types.Scene.sna_animation_panel_enum = bpy.props.EnumProperty(name='Animation Panel Enum', description='', items=[('Cache', 'Cache', '', 0, 0), ('Keyframe', 'Keyframe', '', 0, 1)])
    bpy.types.Scene.sna_rbc_control_menu = bpy.props.PointerProperty(name='RBC Control Menu', description='', type=SNA_GROUP_sna_rbc_control_menu_group)
    bpy.types.Scene.sna_auto_select_rig = bpy.props.BoolProperty(name='Auto Select Rig', description='', default=False)
    bpy.types.Scene.sna_quick_rig_instructions = bpy.props.BoolProperty(name='Quick Rig Instructions', description='', default=False)
    bpy.types.Scene.sna_animation_menu = bpy.props.PointerProperty(name='Animation Menu', description='', type=SNA_GROUP_sna_animation_menu_group)
    bpy.types.Scene.sna_rename_rig = bpy.props.BoolProperty(name='Rename Rig', description='', default=False)
    bpy.types.Scene.sna_rbc_follow_camera = bpy.props.PointerProperty(name='RBC Follow Camera', description='', type=bpy.types.Scene)
    bpy.types.Scene.sna_rbc_chase_camera = bpy.props.PointerProperty(name='RBC Chase Camera', description='', type=bpy.types.Scene)
    bpy.types.Scene.sna_rbw_info = bpy.props.StringProperty(name='RBW Info', description='', default='', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_is_recording = bpy.props.BoolProperty(name='Is Recording', description='', default=False)
    bpy.types.Scene.sna_rbc_rig_asset_list = bpy.props.EnumProperty(name='RBC Rig Asset List', description='', items=sna_rbc_rig_asset_list_enum_items)
    bpy.types.Scene.sna_rbw_speed = bpy.props.FloatProperty(name='RBW Speed', description='', default=0.0, subtype='NONE', unit='NONE', step=3, precision=6)
    bpy.types.Scene.sna_rbc_collection = bpy.props.PointerProperty(name='RBC Collection', description='', type=bpy.types.Collection)
    bpy.types.Scene.sna_rbc_addon_collection = bpy.props.PointerProperty(name='RBC Addon Collection', description='', type=bpy.types.Collection)
    bpy.types.Collection.sna_rbc_asset_collection_properties = bpy.props.PointerProperty(name='RBC Asset Collection Properties', description='', type=SNA_GROUP_sna_rbc_rig_group)
    bpy.types.Collection.sna_rbc_asset_collection = bpy.props.BoolProperty(name='RBC Asset Collection', description='', default=False)
    bpy.types.Scene.sna_speed_unit = bpy.props.EnumProperty(name='Speed Unit', description='', options={'HIDDEN'}, items=[('MPH', 'MPH', 'Values will be calulated by Miles Per Hour', 0, 0), ('Km/h', 'Km/h', 'Values will be calulated by Kilometers Per Hour', 0, 1)])
    bpy.types.Scene.sna_kph = bpy.props.StringProperty(name='KPH', description='', default='', subtype='NONE', maxlen=0)
    bpy.types.Scene.sna_speedometer_menu = bpy.props.PointerProperty(name='Speedometer Menu', description='', type=SNA_GROUP_sna_speedometer_group)
    bpy.types.Scene.sna_scene_rig = bpy.props.CollectionProperty(name='Scene Rig', description='', type=SNA_GROUP_sna_rbc_rig_group)
    bpy.types.Collection.sna_collection_rig = bpy.props.PointerProperty(name='Collection Rig', description='', type=SNA_GROUP_sna_rbc_rig_group)
    bpy.types.Scene.sna_transfer_rig_props = bpy.props.BoolProperty(name='Transfer Rig Props', description='', default=False)
    bpy.types.Scene.sna_asset_placement = bpy.props.EnumProperty(name='Asset Placement', description='', options={'HIDDEN'}, items=[('Center', 'Center', 'Import RBC Asset location to Center', 0, 0), ('Cursor', 'Cursor', 'Import RBC Asset location to Cursor Point', 0, 1)])
    bpy.types.Scene.sna_rbc_scene_ = bpy.props.PointerProperty(name='RBC Scene ', description='', type=SNA_GROUP_sna_rbc_scene_group)
    bpy.types.Scene.sna_a_key_down = bpy.props.BoolProperty(name='A Key down', description='', default=False)
    bpy.types.Scene.sna_d_key_down = bpy.props.BoolProperty(name='D Key Down', description='', default=False)
    bpy.utils.register_class(SNA_OT_Operator_46C07)
    bpy.utils.register_class(SNA_PT_DEV_TOOLS_EC795)
    bpy.utils.register_class(SNA_OT_Dev_Transfer_Props_C5508)
    bpy.utils.register_class(SNA_OT_Add_Rig_Type_B03D7)
    bpy.utils.register_class(SNA_PT_RBC_ADD_RIG_FFA05)
    bpy.utils.register_class(SNA_OT_Quick_Rig_Set__Aa043)
    bpy.utils.register_class(SNA_OT_Quick_Rig_631Dc)
    bpy.utils.register_class(SNA_OT_Modal_Operator_6B7B0)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_220F8)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_BD3FF)
    bpy.utils.register_class(SNA_OT_Rig_To_Cache_4Fb23)
    bpy.utils.register_class(SNA_OT_Rig_To_Animation_91E3F)
    bpy.utils.register_class(SNA_OT_Clear_Baked_Keys_94763)
    bpy.utils.register_class(SNA_OT_Bake_To_Keys_3A4F6)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_7EB4E)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_61194)
    bpy.utils.register_class(SNA_OT_Add_Animation_Objs_5Ca5B)
    bpy.utils.register_class(SNA_OT_Delete_Animation_Objs_5E23A)
    bpy.utils.register_class(SNA_OT_Bake_Ani_Obj_Action_E2073)
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler_0BC89)
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler_E5047)
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler_BC81A)
    bpy.utils.register_class(SNA_OT_Delete_Keyframes_B761F)
    bpy.utils.register_class(SNA_OT_Delete_Baked_Keyframes_03E9D)
    bpy.utils.register_class(SNA_OT_Bake_Keyframes_7F7D6)
    bpy.utils.register_class(SNA_OT_Operator_A72B9)
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler_30ABA)
    bpy.utils.register_class(SNA_PT_NEW_PANEL_7C7C6)
    bpy.utils.register_class(SNA_PT_RBC_ANIMATION_A2B91)
    bpy.utils.register_class(SNA_OT_Modal_Operator_87D5C)
    bpy.utils.register_class(SNA_OT_Insert_Keyframes_6F941)
    bpy.utils.register_class(SNA_OT_Keyframegroup_Ae234)
    bpy.utils.register_class(SNA_OT_Disable_Keyframes_5Fc18)
    bpy.utils.register_class(SNA_OT_Delete_Recorded_Keyframes_F1Cca)
    bpy.utils.register_class(SNA_OT_Show_Keyframes_0C226)
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler_DD6BD)
    bpy.utils.register_class(SNA_OT_Delete_Current_Cache_83F83)
    bpy.utils.register_class(SNA_OT_Playrest_Simulation_0C324)
    bpy.utils.register_class(SNA_OT_Record__Current_Simulation_D1460)
    bpy.utils.register_class(SNA_OT_Record_Simulation_22D2D)
    bpy.utils.register_class(SNA_OT_Transfer_Rbc_Rig_Props_To_Collection_8E3A5)
    bpy.utils.register_class(SNA_OT_Rig_Overlap_Detection_B281A)
    bpy.utils.register_class(SNA_OT_Rig_Placement_84D02)
    bpy.utils.register_class(SNA_PT_RBC_ASSETS_BE12E)
    bpy.utils.register_class(SNA_OT_Import_Rbc_Asset_Rig_5Beb8)
    bpy.utils.register_class(SNA_PT_RBC_COLLISIONS_3D783)
    bpy.utils.register_class(SNA_OT_Clear_Collision_Ops_1F7F2)
    bpy.utils.register_class(SNA_OT_Make_Collision_Passive_Op_8C0C0)
    bpy.utils.register_class(SNA_OT_Make_Collision_Active_Op_38F01)
    bpy.types.PHYSICS_PT_rigid_body_collisions.prepend(sna_add_to_physics_pt_rigid_body_collisions_027B3)
    bpy.utils.register_class(SNA_OT_Show_Convex_Hull_Aab03)
    bpy.utils.register_class(SNA_PT_RIGID_BODY_WORLD_9E69D)
    bpy.utils.register_class(SNA_OT_Refresh_Rbc_Collection2_Abaaf)
    bpy.utils.register_class(SNA_OT_Delete_Rbc_Rig__0De67)
    bpy.app.handlers.load_pre.append(load_pre_handler_1F36E)
    bpy.utils.register_class(SNA_OT_Refresh_Rbc_Collection_Bf32F)
    bpy.utils.register_class(SNA_PT_RBC_COLLECTION_8ECBE)
    bpy.utils.register_class(SNA_OT_Import_Xinput_A1516)
    bpy.utils.register_class(SNA_OT_Controller_Operator_Fe555)
    bpy.utils.register_class(SNA_OT_Wasd_Modal_E6557)
    bpy.utils.register_class(SNA_OT_Drive_Reset_D354C)
    bpy.utils.register_class(SNA_OT_Steering_Reset_Ae4F6)
    bpy.utils.register_class(SNA_OT_Speedometers_25082)
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler_9AC38)
    bpy.utils.register_class(SNA_OT_Reset_Suspension_Limits_E12Bd)
    bpy.utils.register_class(SNA_OT_Reset_Spring_Stiffness_F75A8)
    bpy.utils.register_class(SNA_OT_Reset_Spring_Damping_Ce584)
    bpy.utils.register_class(SNA_OT_Reset_Motor_Torque_D3852)
    bpy.utils.register_class(SNA_OT_Reset_Pivot_Points_8F3E7)
    bpy.utils.register_class(SNA_OT_Reset_Turn_Radius_B505E)
    bpy.utils.register_class(SNA_OT_Reset_Caster_Angle_Bbefb)
    bpy.utils.register_class(SNA_OT_Reset_Weight_Position_2Fbd2)
    bpy.utils.register_class(SNA_OT_Reset_Roll_Constraint_Eb720)
    bpy.utils.register_class(SNA_OT_Reset_Tire_Friction_A0520)
    bpy.utils.register_class(SNA_OT_Reset_Weight_3D40F)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_CFF48)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_87138)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_B5700)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_EE4B7)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_A3B96)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_C5D97)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_9218D)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_EE3CA)
    bpy.utils.register_class(SNA_PT_RBC_RIG_0A7A5)
    bpy.utils.register_class(SNA_OT_Add_Ground_28971)
    bpy.app.handlers.frame_change_pre.append(frame_change_pre_handler_156BA)
    bpy.utils.register_class(SNA_OT_Offset_Active_Rig_Location_Op_3614B)
    bpy.utils.register_class(SNA_OT_Remove_Constraints_Bc322)
    bpy.utils.register_class(SNA_PT_NEW_PANEL_9119D)
    bpy.types.PHYSICS_PT_add.append(sna_add_to_physics_pt_add_1E465)
    bpy.types.PHYSICS_PT_rigid_body_constraint_objects.append(sna_add_to_physics_pt_rigid_body_constraint_objects_E7853)
    bpy.utils.register_class(SNA_OT_Copy_Selected_Constraints_9629A)
    bpy.utils.register_class(SNA_OT_Switch_Objects_8B723)
    bpy.utils.register_class(SNA_OT_Clear_Rig_Control_Constraints_2322E)
    bpy.utils.register_class(SNA_OT_Reset_Rb_Obj_Buttons_2603E)
    bpy.utils.register_class(SNA_OT_Reset_Rb_Obj_Location_D2903)
    bpy.utils.register_class(SNA_OT_Parent_Modelcollection_28104)
    bpy.utils.register_class(SNA_OT_Clear_Rig_4Ed9B)
    bpy.utils.register_class(SNA_OT_Clear_Model_Constraints_43579)
    bpy.utils.register_class(SNA_OT_Generate_Rig_6C502)
    bpy.utils.register_class(SNA_OT_Rig_Tune_Up_Be9A4)
    bpy.utils.register_class(SNA_OT_Snap_To_Ground_F6C01)
    bpy.utils.register_class(SNA_OT_Is_Empty_46D86)
    bpy.utils.register_class(SNA_OT_Create_Convex_Hull_78B8A)
    bpy.utils.register_class(SNA_OT_Set_Weight_Position__74A84)
    bpy.app.handlers.frame_change_post.append(frame_change_post_handler_73628)
    bpy.utils.register_class(SNA_PT_RIGID_BODY_SETTINGS_45887)
    bpy.utils.register_class(SNA_PT_PERFORMANCE_74559)


def unregister():
    global _icons
    bpy.utils.previews.remove(_icons)
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    for km, kmi in addon_keymaps.values():
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    del bpy.types.Scene.sna_d_key_down
    del bpy.types.Scene.sna_a_key_down
    del bpy.types.Scene.sna_rbc_scene_
    del bpy.types.Scene.sna_asset_placement
    del bpy.types.Scene.sna_transfer_rig_props
    del bpy.types.Collection.sna_collection_rig
    del bpy.types.Scene.sna_scene_rig
    del bpy.types.Scene.sna_speedometer_menu
    del bpy.types.Scene.sna_kph
    del bpy.types.Scene.sna_speed_unit
    del bpy.types.Collection.sna_rbc_asset_collection
    del bpy.types.Collection.sna_rbc_asset_collection_properties
    del bpy.types.Scene.sna_rbc_addon_collection
    del bpy.types.Scene.sna_rbc_collection
    del bpy.types.Scene.sna_rbw_speed
    del bpy.types.Scene.sna_rbc_rig_asset_list
    del bpy.types.Scene.sna_is_recording
    del bpy.types.Scene.sna_rbw_info
    del bpy.types.Scene.sna_rbc_chase_camera
    del bpy.types.Scene.sna_rbc_follow_camera
    del bpy.types.Scene.sna_rename_rig
    del bpy.types.Scene.sna_animation_menu
    del bpy.types.Scene.sna_quick_rig_instructions
    del bpy.types.Scene.sna_auto_select_rig
    del bpy.types.Scene.sna_rbc_control_menu
    del bpy.types.Scene.sna_animation_panel_enum
    del bpy.types.Object.sna_rotdata
    del bpy.types.Scene.sna_locdata
    del bpy.types.Scene.sna_overlap_bool
    del bpy.types.Scene.sna_rbc_ground_plane
    del bpy.types.Scene.sna_active_rig
    del bpy.types.Object.sna_rig_control_drivers
    del bpy.types.Scene.sna_rig_tuning_menu
    del bpy.types.Scene.sna_rig_tuning_enum
    del bpy.types.Scene.sna_rig_control_panel
    del bpy.types.Scene.sna_custom_vehicle_set
    del bpy.types.Scene.sna_set_up_preview
    del bpy.types.Object.sna_control_rig_car_bodies
    del bpy.types.Object.sna_body_axles
    del bpy.types.Scene.sna_rbc_rig_panel_icon
    del bpy.types.Scene.sna_rbc_rig_panel
    del bpy.types.Scene.sna_rbc_set_up_advanced
    del bpy.types.Scene.sna_rbc_rig_type_menu
    del bpy.types.Scene.sna_rbc_collection_list
    del bpy.types.Scene.sna_rbc_rig_collection
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_axle_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_rig_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_scene_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_speedometer_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rig_guides_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_animation_menu_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rig_tuning_all_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_control_menu_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rig_tuning_menu_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rig_tuning_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rig_drivers_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_custom_vehicle_properties)
    bpy.utils.unregister_class(SNA_GROUP_sna_vehicle_preview_propeties)
    bpy.utils.unregister_class(SNA_GROUP_sna_set_up_preview_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_body_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_wheel_group)
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_objs)
    bpy.utils.unregister_class(SNA_GROUP_sna_rbc_setup_advanced_group)
    bpy.utils.unregister_class(SNA_OT_Operator_46C07)
    bpy.utils.unregister_class(SNA_PT_DEV_TOOLS_EC795)
    bpy.utils.unregister_class(SNA_OT_Dev_Transfer_Props_C5508)
    bpy.utils.unregister_class(SNA_OT_Add_Rig_Type_B03D7)
    bpy.utils.unregister_class(SNA_PT_RBC_ADD_RIG_FFA05)
    bpy.utils.unregister_class(SNA_OT_Quick_Rig_Set__Aa043)
    bpy.utils.unregister_class(SNA_OT_Quick_Rig_631Dc)
    bpy.utils.unregister_class(SNA_OT_Modal_Operator_6B7B0)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_220F8)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_BD3FF)
    bpy.utils.unregister_class(SNA_OT_Rig_To_Cache_4Fb23)
    bpy.utils.unregister_class(SNA_OT_Rig_To_Animation_91E3F)
    bpy.utils.unregister_class(SNA_OT_Clear_Baked_Keys_94763)
    bpy.utils.unregister_class(SNA_OT_Bake_To_Keys_3A4F6)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_7EB4E)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_61194)
    bpy.utils.unregister_class(SNA_OT_Add_Animation_Objs_5Ca5B)
    bpy.utils.unregister_class(SNA_OT_Delete_Animation_Objs_5E23A)
    bpy.utils.unregister_class(SNA_OT_Bake_Ani_Obj_Action_E2073)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler_0BC89)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler_E5047)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler_BC81A)
    bpy.utils.unregister_class(SNA_OT_Delete_Keyframes_B761F)
    bpy.utils.unregister_class(SNA_OT_Delete_Baked_Keyframes_03E9D)
    bpy.utils.unregister_class(SNA_OT_Bake_Keyframes_7F7D6)
    bpy.utils.unregister_class(SNA_OT_Operator_A72B9)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler_30ABA)
    bpy.utils.unregister_class(SNA_PT_NEW_PANEL_7C7C6)
    bpy.utils.unregister_class(SNA_PT_RBC_ANIMATION_A2B91)
    bpy.utils.unregister_class(SNA_OT_Modal_Operator_87D5C)
    bpy.utils.unregister_class(SNA_OT_Insert_Keyframes_6F941)
    bpy.utils.unregister_class(SNA_OT_Keyframegroup_Ae234)
    bpy.utils.unregister_class(SNA_OT_Disable_Keyframes_5Fc18)
    bpy.utils.unregister_class(SNA_OT_Delete_Recorded_Keyframes_F1Cca)
    bpy.utils.unregister_class(SNA_OT_Show_Keyframes_0C226)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler_DD6BD)
    bpy.utils.unregister_class(SNA_OT_Delete_Current_Cache_83F83)
    bpy.utils.unregister_class(SNA_OT_Playrest_Simulation_0C324)
    bpy.utils.unregister_class(SNA_OT_Record__Current_Simulation_D1460)
    bpy.utils.unregister_class(SNA_OT_Record_Simulation_22D2D)
    bpy.utils.unregister_class(SNA_OT_Transfer_Rbc_Rig_Props_To_Collection_8E3A5)
    bpy.utils.unregister_class(SNA_OT_Rig_Overlap_Detection_B281A)
    bpy.utils.unregister_class(SNA_OT_Rig_Placement_84D02)
    bpy.utils.unregister_class(SNA_PT_RBC_ASSETS_BE12E)
    bpy.utils.unregister_class(SNA_OT_Import_Rbc_Asset_Rig_5Beb8)
    bpy.utils.unregister_class(SNA_PT_RBC_COLLISIONS_3D783)
    bpy.utils.unregister_class(SNA_OT_Clear_Collision_Ops_1F7F2)
    bpy.utils.unregister_class(SNA_OT_Make_Collision_Passive_Op_8C0C0)
    bpy.utils.unregister_class(SNA_OT_Make_Collision_Active_Op_38F01)
    bpy.types.PHYSICS_PT_rigid_body_collisions.remove(sna_add_to_physics_pt_rigid_body_collisions_027B3)
    bpy.utils.unregister_class(SNA_OT_Show_Convex_Hull_Aab03)
    bpy.utils.unregister_class(SNA_PT_RIGID_BODY_WORLD_9E69D)
    bpy.utils.unregister_class(SNA_OT_Refresh_Rbc_Collection2_Abaaf)
    bpy.utils.unregister_class(SNA_OT_Delete_Rbc_Rig__0De67)
    bpy.app.handlers.load_pre.remove(load_pre_handler_1F36E)
    bpy.utils.unregister_class(SNA_OT_Refresh_Rbc_Collection_Bf32F)
    bpy.utils.unregister_class(SNA_PT_RBC_COLLECTION_8ECBE)
    bpy.utils.unregister_class(SNA_OT_Import_Xinput_A1516)
    bpy.utils.unregister_class(SNA_OT_Controller_Operator_Fe555)
    bpy.utils.unregister_class(SNA_OT_Wasd_Modal_E6557)
    bpy.utils.unregister_class(SNA_OT_Drive_Reset_D354C)
    bpy.utils.unregister_class(SNA_OT_Steering_Reset_Ae4F6)
    bpy.utils.unregister_class(SNA_OT_Speedometers_25082)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler_9AC38)
    bpy.utils.unregister_class(SNA_OT_Reset_Suspension_Limits_E12Bd)
    bpy.utils.unregister_class(SNA_OT_Reset_Spring_Stiffness_F75A8)
    bpy.utils.unregister_class(SNA_OT_Reset_Spring_Damping_Ce584)
    bpy.utils.unregister_class(SNA_OT_Reset_Motor_Torque_D3852)
    bpy.utils.unregister_class(SNA_OT_Reset_Pivot_Points_8F3E7)
    bpy.utils.unregister_class(SNA_OT_Reset_Turn_Radius_B505E)
    bpy.utils.unregister_class(SNA_OT_Reset_Caster_Angle_Bbefb)
    bpy.utils.unregister_class(SNA_OT_Reset_Weight_Position_2Fbd2)
    bpy.utils.unregister_class(SNA_OT_Reset_Roll_Constraint_Eb720)
    bpy.utils.unregister_class(SNA_OT_Reset_Tire_Friction_A0520)
    bpy.utils.unregister_class(SNA_OT_Reset_Weight_3D40F)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_CFF48)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_87138)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_B5700)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_EE4B7)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_A3B96)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_C5D97)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_9218D)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_EE3CA)
    bpy.utils.unregister_class(SNA_PT_RBC_RIG_0A7A5)
    bpy.utils.unregister_class(SNA_OT_Add_Ground_28971)
    bpy.app.handlers.frame_change_pre.remove(frame_change_pre_handler_156BA)
    bpy.utils.unregister_class(SNA_OT_Offset_Active_Rig_Location_Op_3614B)
    bpy.utils.unregister_class(SNA_OT_Remove_Constraints_Bc322)
    bpy.utils.unregister_class(SNA_PT_NEW_PANEL_9119D)
    bpy.types.PHYSICS_PT_add.remove(sna_add_to_physics_pt_add_1E465)
    bpy.types.PHYSICS_PT_rigid_body_constraint_objects.remove(sna_add_to_physics_pt_rigid_body_constraint_objects_E7853)
    bpy.utils.unregister_class(SNA_OT_Copy_Selected_Constraints_9629A)
    bpy.utils.unregister_class(SNA_OT_Switch_Objects_8B723)
    bpy.utils.unregister_class(SNA_OT_Clear_Rig_Control_Constraints_2322E)
    bpy.utils.unregister_class(SNA_OT_Reset_Rb_Obj_Buttons_2603E)
    bpy.utils.unregister_class(SNA_OT_Reset_Rb_Obj_Location_D2903)
    bpy.utils.unregister_class(SNA_OT_Parent_Modelcollection_28104)
    bpy.utils.unregister_class(SNA_OT_Clear_Rig_4Ed9B)
    bpy.utils.unregister_class(SNA_OT_Clear_Model_Constraints_43579)
    bpy.utils.unregister_class(SNA_OT_Generate_Rig_6C502)
    bpy.utils.unregister_class(SNA_OT_Rig_Tune_Up_Be9A4)
    bpy.utils.unregister_class(SNA_OT_Snap_To_Ground_F6C01)
    bpy.utils.unregister_class(SNA_OT_Is_Empty_46D86)
    bpy.utils.unregister_class(SNA_OT_Create_Convex_Hull_78B8A)
    bpy.utils.unregister_class(SNA_OT_Set_Weight_Position__74A84)
    bpy.app.handlers.frame_change_post.remove(frame_change_post_handler_73628)
    bpy.utils.unregister_class(SNA_PT_RIGID_BODY_SETTINGS_45887)
    bpy.utils.unregister_class(SNA_PT_PERFORMANCE_74559)

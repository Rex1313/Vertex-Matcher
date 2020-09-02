bl_info = {
    "name": "Vertex Matcher",
    "description": "Matches Vertex position on one or more axis",
    "author": "Sylwester Moniuszko-Szymanski",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Modeling"
}


import bpy
import bmesh

from bpy.props import (BoolProperty,
                       PointerProperty
                       )
from bpy.types import (Panel,
                       PropertyGroup,
                       Operator
                       )

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class VertexMatcherProperties(PropertyGroup):

    x_axis: BoolProperty(
        name="X",
        description="Match Vertex on X axis",
        default = False
        )
        
    y_axis: BoolProperty(
        name="Y",
        description="Match Vertex on Y axis",
        default = False
        )
        
    z_axis: BoolProperty(
        name="Z",
        description="Match Vertex on Z axis",
        default = False
        )


def matchVertex(axis):
    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    print(axis)
    def get_axis(elem):
        switcher = {
            'x': elem.co.x,
            'y': elem.co.y,
            'z': elem.co.z
        }
        return switcher.get(axis,"Nothing")
    def set_axis(first,elem):
       if(axis=='x'):
          elem.co.x = first.co.x
       if(axis=='y'):
          elem.co.y = first.co.y
       if(axis=='z'):
          elem.co.z = first.co.z
    last_vertex = None
    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMVert):
           last_vertex = elem
           break   
    for elem in bm.select_history:
        set_axis(last_vertex, elem)   
        
#different selection
    selected_verts = list(filter(lambda v: v.select, bm.verts))
    if(last_vertex == None):
        last_vertex = selected_verts[-1] 
    for elem in reversed(selected_verts):
        set_axis(last_vertex, elem)     
        
#Used to insntantly see the result in editor    
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.mode_set(mode = 'EDIT')   

# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_VertexMatcher(Operator):
    bl_label = "Match Vertex Position"
    bl_idname = "wm.vertex_matcher"
    
    def execute(self, context):
        scene = bpy.context.scene
        v_matcher = scene.vertex_matcher
        if(v_matcher.x_axis==True):
            matchVertex('x')
        if(v_matcher.y_axis==True):
            matchVertex('y')
        if(v_matcher.z_axis==True):
            matchVertex('z')
        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Panel in Edit Mode
# ------------------------------------------------------------------------

class OBJECT_PT_VertexPanel(Panel):
    bl_label = "Vertex Matcher"
    bl_idname = "OBJECT_PT_vertex_matcher"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Vertex Tools"
    bl_context = "mesh_edit"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = bpy.context.scene
        mytool = scene.vertex_matcher
        layout.prop(mytool, "x_axis")
        layout.separator()
        layout.prop(mytool, "y_axis")
        layout.separator() 
        layout.prop(mytool, "z_axis")
        layout.operator("wm.vertex_matcher")
        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    VertexMatcherProperties,
    WM_OT_VertexMatcher,
    OBJECT_PT_VertexPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.vertex_matcher = PointerProperty(type=VertexMatcherProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.vertex_matcher

bl_info = {
    "name" : "文本管理",
    "author" : "尐贤之辈のTENO",
    "description" : "管理文本",
    "blender" : (3, 6, 0),
    "version" : (1, 0, 0),
    "location" : "TEXT > tma",
    "category" : "Text",
    "doc_url": "",
    "tracker_url": "https://space.bilibili.com/1729654169"
}
import bpy
from bpy.types import PropertyGroup,Operator,Panel
from bpy.props import (
        IntProperty,
        BoolProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty,
        FloatProperty,
        IntVectorProperty,
        EnumProperty,
        CollectionProperty
    )
    
class TMA_MT_Error_menu(bpy.types.Menu):
    bl_label = "错误"
    bl_idname = "TMA_MT_Error_menu"

    def draw(self, context):
        layout = self.layout
        layout.label(text=error_thing,icon="ERROR")
def rl(naming=TMA_MT_Error_menu):
    bpy.ops.wm.call_menu(name=naming.bl_idname)
    
    
def group_index(s):
    tools=bpy.context.scene.tma
    return list(tools.group).index(s)
def text_index(s):
    for i in bpy.context.scene.tma.group:
        try:
            t=list(i.text).index(s)
            return i,t
        except:
            continue
def rename_op(self,context):
    if not self.rename_op:
        return
    global item
    item=self
    self.rename_op=False
    bpy.ops.tma.grouprename("INVOKE_DEFAULT")
def remove_op_group(self,context):
    global item
    item=self
    bpy.ops.tma.remove(type="GROUP")
def new_text(self,context):
    if not self.new_text:
        return
    global item
    item=self
    bpy.ops.tma.newone(type="TEXT")
    self.new_text=False
def open_op(self,context):
    if not self.open_op:
        return
    if self.object is None:
        self.open_op=False
        return
    context.space_data.text=self.object
    self.open_op=False
def remove_op_text(self,context):
    global item
    item=self
    bpy.ops.tma.remove(type="TEXT")
def up_op_group(self,context):
    if not self.up_op:
        return
    tools=context.scene.tma
    Index=group_index(self)
    self.up_op=False
    context.scene.tma.group.move(Index,Index-1)
def down_op_group(self,context):
    if not self.down_op:
        return
    tools=context.scene.tma
    Index=group_index(self)
    self.down_op=False
    if len(list(tools.group))==1:
        return
    tools.group.move(Index,Index+1)
def up_op_text(self,context):
    if not self.up_op:
        return
    i,t=text_index(self)
    i1=i.text[t-1].object
    i2=i.text[t].object
    i.text[t-1].object=i2
    i.text[t].object=i1
    self.up_op=False
def down_op_text(self,context):
    if not self.down_op:
        return
    i,t=text_index(self)
    if len(list(i.text))==1:
        self.down_op=False
        return
    i1=i.text[t+1].object
    i2=i.text[t].object
    i.text[t+1].object=i2
    i.text[t].object=i1
    self.down_op=False
def change_group(self,context):
    if not self.change_group:
        return
    global item
    item=self
    self.change_group=False
    bpy.ops.tma.changegroup("INVOKE_DEFAULT")
class Text(PropertyGroup):
    object : PointerProperty(type=bpy.types.Text,name="文本")
    open_op : BoolProperty(update=open_op,name="在文本编辑器中打开")
    up_op : BoolProperty(update=up_op_text,name="上移")
    down_op : BoolProperty(update=down_op_text,name="下移")
    remove_op : BoolProperty(update=remove_op_text,name="移除")
    change_group : BoolProperty(update=change_group,name="换组")
class Group(PropertyGroup):
    name : StringProperty()
    show_rename : BoolProperty(name="设置重命名")
    rename : StringProperty(name="重命名")
    hidenshow_op : BoolProperty()
    rename_op : BoolProperty(update=rename_op,name="应用重命名")
    up_op : BoolProperty(update=up_op_group,name="上移")
    down_op : BoolProperty(update=down_op_group,name="下移")
    remove_op : BoolProperty(update=remove_op_group,name="移除")
    text : CollectionProperty(type=Text,name="")
    new_text : BoolProperty(update=new_text,name="")
class Var(PropertyGroup):
    group : CollectionProperty(type=Group)
class changegroup(Operator):
    bl_idname="tma.changegroup"
    bl_label="换组"
    #bl_options={"REGISTER","UNDO"}
    change : StringProperty(name="换至")
    def draw(self,context):
        tools=context.scene.tma
        row=self.layout.row()
        row.prop_search(self,"change",tools,"group")
    def execute(self,context):
        tools=context.scene.tma
        try:
            g_index=[e.name for e in tools.group].index(self.change)
        except:
            global error_thing
            error_thing="找不到组"
            rl()
            self.report({"ERROR"},"找不到组")
            return {"FINISHED"}
        i,t=text_index(item)
        ob=item.object
        i.text.remove(t)
        tools.group[g_index].text.add().object=ob
        return {"FINISHED"}
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self, width=280)
class grouprename(Operator):
    bl_idname="tma.grouprename"
    bl_label="组重命名（不能取重复名字）"
    #bl_options={"REGISTER","UNDO"}
    def execute(self,context):
        tools=context.scene.tma
        n=[e.name for e in tools.group]
        if item.rename in n:
            global error_thing
            error_thing="不能重名"
            rl()
            return {"FINISHED"}
        item.name=item.rename
        item.show_rename=False
        return {"FINISHED"}
class newone(Operator):
    bl_idname="tma.newone"
    bl_label="新建"
    bl_options={"REGISTER","UNDO"}
    type : StringProperty()
    def execute(self,context):
        tools=context.scene.tma
        if self.type=="GROUP":
            n=[e.name for e in tools.group]
            name="NEW ONE"
            while name in n:
                name+=" N"
            tools.group.add().name=name
        if self.type=="TEXT":
            item.text.add()
        return {"FINISHED"}
class remove(Operator):
    bl_idname="tma.remove"
    bl_label="移除"
    bl_options={"REGISTER","UNDO"}
    type : StringProperty()
    def execute(self,context):
        tools=context.scene.tma
        if self.type=="GROUP":
            tools.group.remove(group_index(item))
        if self.type=="TEXT":
            i,t=text_index(item)
            i.text.remove(t)
        return {"FINISHED"}
                
                
class TMA_PT_textpanel_panel(Panel):
    bl_space_type = 'TEXT_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Text"
    bl_idname = "TMA_PT_textpanel_panel"
    bl_label = "文本管理"
    def draw(self,context):
        layout=self.layout
        tools=context.scene.tma
        for c1,i in enumerate(tools.group):
            col=layout.column(align=True)
            row=col.row(align=True)
            row.prop(i,"hidenshow_op",text=i.name,icon="TRIA_DOWN" if i.hidenshow_op else "TRIA_RIGHT")
            row.prop(i,"show_rename",icon="ANCHOR_RIGHT",text="")
            rowx=row.row(align=True)
            rowx.prop(i,"up_op",icon="TRIA_UP",text="")
            if c1==0:
                rowx.enabled=False
            L=len(list(tools.group))
            rowy=row.row(align=True)
            rowy.prop(i,"down_op",icon="TRIA_DOWN",text="")
            if c1==L-1 or L==1:
                rowy.enabled=False
            row=row.row(align=True)
            row.prop(i,"remove_op",icon="REMOVE",text="")
            if i.show_rename:
                box0=self.layout.box().row(align=True)
                box0.prop(i,"rename",text="")
                box0.prop(i,"rename_op",icon="TEXT",text="")
            if i.hidenshow_op:
                box1=self.layout.box().column()
                box1.prop(i,"new_text",text="新建文本预览",icon="ADD")
                for c2,o in enumerate(i.text):
                    box=box1.row(align=True)
                    box.prop(o,"object",text="")
                    box.prop(o,"open_op",icon="TEXT",text="")
                    boxx=box.row(align=True)
                    boxx.prop(o,"up_op",icon="TRIA_UP",text="")
                    if c2==0:
                        boxx.enabled=False
                    L=len(list(i.text))
                    boxy=box.row(align=True)
                    boxy.prop(o,"down_op",icon="TRIA_DOWN",text="")
                    if c2==L-1 or L==1:
                        boxy.enabled=False
                    box=box.row(align=True)
                    box.prop(o,"remove_op",icon="REMOVE",text="")
                    box.prop(o,"change_group",icon="MOD_TRIANGULATE",text="")
                
        self.layout.operator(newone.bl_idname,text="新建组预览").type="GROUP"


c=(
    TMA_MT_Error_menu,
    Text,
    Group,
    Var,
    grouprename,
    newone,
    remove,
    changegroup,
    TMA_PT_textpanel_panel
)
def register():
    for i in c:
        #print(i)
        bpy.utils.register_class(i)
    bpy.types.Scene.tma=PointerProperty(type=Var)
def unregister():
    for i in c:
        bpy.utils.unregister_class(i)
    del bpy.types.Scene.tma
if __name__=="__main__":
    register()
    
    
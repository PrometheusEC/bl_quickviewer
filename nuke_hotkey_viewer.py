bl_info = {
    "name": "Nuke Hotkey Viewer",
    "author": "Edgar Aguirre",
    "version": (1, 0),
    "blender": (4, 5, 6),
    "location": "Compositor",
    "description": "Assign nodes to number keys and send them to viewer. "
    "Shift + number to store, number to view",
    "category": "Node",
}

import bpy

NUMBER_KEYS = {
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX",
    7: "SEVEN",
    8: "EIGHT",
    9: "NINE",
}

viewer_slots = {}


def get_viewer_node(tree):
    for node in tree.nodes:
        if node.type == 'VIEWER':
            return node

    viewer = tree.nodes.new("CompositorNodeViewer")
    viewer.location = (500, 0)
    return viewer


class NODE_OT_store_viewer_slot(bpy.types.Operator):
    bl_idname = "node.store_viewer_slot"
    bl_label = "Store Viewer Slot"

    slot: bpy.props.IntProperty()

    def execute(self, context):

        node = context.active_node

        if not node:
            self.report({'WARNING'}, "No active node")
            return {'CANCELLED'}

        viewer_slots[self.slot] = node.name

        self.report({'INFO'}, f"Stored {node.name} in slot {self.slot}")

        return {'FINISHED'}


class NODE_OT_view_viewer_slot(bpy.types.Operator):
    bl_idname = "node.view_viewer_slot"
    bl_label = "View Viewer Slot"

    slot: bpy.props.IntProperty()

    def execute(self, context):

        tree = context.scene.node_tree

        if not tree:
            return {'CANCELLED'}

        node_name = viewer_slots.get(self.slot)

        if not node_name:
            self.report({'WARNING'}, "Slot empty")
            return {'CANCELLED'}

        node = tree.nodes.get(node_name)

        viewer = get_viewer_node(tree)

        tree.links.new(node.outputs[0], viewer.inputs[0])

        return {'FINISHED'}


addon_keymaps = []


def register_hotkeys():

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if not kc:
        return

    km = kc.keymaps.new(name="Node Editor", space_type="NODE_EDITOR")

    for i in range(1, 10):

        kmi = km.keymap_items.new(
            "node.view_viewer_slot",
            type=NUMBER_KEYS[i],
            value="PRESS"
        )
        kmi.properties.slot = i
        addon_keymaps.append((km, kmi))

        kmi = km.keymap_items.new(
            "node.store_viewer_slot",
            type=NUMBER_KEYS[i] ,
            value="PRESS",
            shift=True
        )
        kmi.properties.slot = i
        addon_keymaps.append((km, kmi))


def unregister_hotkeys():

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)

    addon_keymaps.clear()


classes = (
    NODE_OT_store_viewer_slot,
    NODE_OT_view_viewer_slot,
)


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    register_hotkeys()


def unregister():

    unregister_hotkeys()

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
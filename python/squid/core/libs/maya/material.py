# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from maya import cmds


def get_connected_all_files(target):
    u"""指定したノードを基点に全てのファイルノードを取得

    Args:
        target (unicode): 対象

    Returns:
        list of unicode: 対象のノードを基点として接続されている全てのファイルノードのリストを返す
    """
    result = []
    result.extend(get_connected_files(target))

    result.extend(get_files_via_shading_depend_node(target, "layeredTexture"))

    result.extend(get_files_via_shading_depend_node(target, "bump2d"))

    return result


def get_files_via_shading_depend_node(target, via_type):
    u"""ShadingDependNodeを経由して接続されているファイルノードを返す

    Args:
        target (unicode): 対象
        via_type (str): ShadingDependNode

    Returns:
        list of unicode: ShadingDependNodeを経由して接続されているファイルノードのリスト
    """
    result = []
    shading_depend_nodes = cmds.listConnections(target, type=via_type)
    if not shading_depend_nodes:
        return result
    for b in shading_depend_nodes:
        result.extend(get_connected_files(b))
    return result


def get_connected_files(target):
    u"""対象のノードに接続されているファイルノードのリストを返す

    Args:
        target (unicode): 対象

    Returns:
        list of unicode: 対象のノードに接続されているファイルノードのリスト
    """
    result = []
    files = cmds.listConnections(target, type="file")
    if not files:
        return result
    return list(set(files))


def get_transforms_from_material(material, full=False):
    u"""Materialをもとに適用されているtransformのリストを返す
    
    Args:
        material (unicode): 対象のMaterial
        full (bool): フルパスで返すかどうか

    Returns:
        list of unicode: 指定Materialが適用されているtransformのリストを返す
    """
    result = set()
    connections = cmds.listConnections(material, d=True)
    for connection in connections:
        if cmds.objectType(connection) == "shadingEngine":
            tmp = cmds.listConnections(connection + ".dagSetMembers", s=True)
            if tmp:
                # オブジェクトにMaterial適用->フェースに別Material適用->フェースにオブジェクトと同じMaterial適用
                # というフローを踏んだとき、dagSetMembersに同じtransformが複数登録され得るので、setで一意にする
                if full:
                    tmp = cmds.ls(tmp, l=full)
                result = set([x for x in tmp if cmds.objectType(x) == "transform"])

    return result


def get_necessary_file_nodes(transform_set, full=False):
    u"""指定したtransformのSetに必要なファイルノードのリストを返す

    Args:
        transform_set (set of unicode): transformのセット
        full (bool): transform_setがフルパスかどうか

    Returns:
        set of unicode: ファイルノードのセット
    """
    result = []
    for mat in cmds.ls(mat=True, ni=True):
        res = get_transforms_from_material(mat, full=full)
        if not transform_set.intersection(res):
            continue
        result.extend(get_connected_all_files(mat))
    return set(result)


def get_material_from_transform(transforms, full_path=False):
    u"""指定transform配下に適用されているMaterialを返す

    Args:
        transforms (list of unicode): transformのリスト
        full_path (bool): transformsがフルパスかどうか

    Returns:
        list of unicode: Materialのリスト
    """
    res = []
    materials = cmds.ls(mat=True)
    for material in materials:
        connections = cmds.listConnections(material, d=True, type="shadingEngine")
        for c in connections:
            members = cmds.listConnections(c + ".dagSetMembers", s=True)
            if not members:
                continue
            members = cmds.ls(members, l=full_path)
            for m in members:
                if m not in transforms:
                    continue
                res.append(material)
    return list(set(res))


def get_material_from_mesh_transform(transform):
    u"""指定transformのmeshに適用されているMaterialのリストを返す

    Args:
        transform (unicode): meshを持つtransform

    Returns:
        list of unicode: 指定transformのmeshに適用されているMaterialのリスト
    """
    mesh = cmds.listRelatives(transform, shapes=True, ni=True, f=True)[0]
    if not mesh:
        return []
    shading_engine = cmds.listConnections(mesh, type="shadingEngine")
    if not shading_engine:
        return []
    return list(set(cmds.ls(cmds.listConnections(shading_engine, d=False), mat=True)))


def extract_faces_target_material_assigned(shape, mat):
    u"""指定Materialが割当されてるフェースを抽出して返す

    Args:
        shape (unicode): 対象のShape
        mat (unicode): 対象のMaterial

    Returns:
        指定Materialが割当されてるフェースのリスト
    """
    root_obj_group = "{0}.instObjGroups[0]".format(shape)
    root_shading_engines = cmds.listConnections(root_obj_group, type="shadingEngine")
    if root_shading_engines:
        if not cmds.listConnections(root_shading_engines[0] + ".surfaceShader"):
            return cmds.ls(shape + ".f[*]", fl=1)
        return []
    indices = cmds.getAttr(root_obj_group + ".objectGroups", mi=True)
    mat_assigned_faces = []
    if not indices:
        return mat_assigned_faces
    for i in indices:
        obj_group = "{0}.instObjGroups[0].objectGroups[{1}]".format(shape, str(i))
        shading_engines = cmds.listConnections(obj_group, type="shadingEngine")
        if not shading_engines:
            continue
        faces = cmds.getAttr(obj_group + ".objectGrpCompList")
        if not faces:
            continue
        shader = cmds.listConnections(shading_engines[0] + ".surfaceShader")[0]
        if shader != mat:
            continue
        for f in faces:
            mat_assigned_faces.extend(cmds.ls(shape + "." + f, fl=True))
    return mat_assigned_faces


def extract_objects_target_material_assigned(shape):
    u"""指定されたShapeに接続されたMaterialとフェース情報を返す
    
    Args:
        shape (unicode): 対象のShape

    Returns:
        unicode, list: オブジェクト自体に適用されたMaterial名、フェースと適用されたMaterialのリスト
    """
    base_material = get_material_assigned_to_shape(shape)
    assigned_faces = []
    root_obj_group = "{0}.instObjGroups[0]".format(shape)
    indices = cmds.getAttr(root_obj_group + ".objectGroups", mi=True)
    if not indices:
        print("33333")
        return base_material, assigned_faces
    for i in indices:
        obj_group = "{0}.instObjGroups[0].objectGroups[{1}]".format(shape, str(i))
        shading_engines = cmds.listConnections(obj_group, type="shadingEngine")
        if not shading_engines:
            continue
        faces = cmds.getAttr(obj_group + ".objectGrpCompList")
        if not faces:
            continue
        mat = cmds.listConnections(shading_engines[0] + ".surfaceShader")[0]
        for f in faces:
            assigned_faces.append((mat, cmds.ls(shape + "." + f, fl=True)))
    return base_material, assigned_faces


def get_material_assigned_to_shape(shape):
    u"""Shape自体に適用されたMaterialを返す

    Args:
        shape (unicode): 対象のShape

    Returns:
        unicode: Shape自体に適用されたMaterial
    """
    root_obj_group = "{0}.compInstObjGroups[0]".format(shape)
    indices = cmds.getAttr(root_obj_group + ".compObjectGroups", mi=True)
    if not indices:
        root_obj_group = "{0}.instObjGroups[0]".format(shape)
        root_shading_engines = cmds.listConnections(root_obj_group, type="shadingEngine")
        if root_shading_engines:
            shader = cmds.listConnections(root_shading_engines[0] + ".surfaceShader")
            if not shader:
                return None
            return shader[0]
        return None
    obj_group = "{0}.compInstObjGroups[0].compObjectGroups[{1}]".format(shape, str(indices[0]))
    shading_engines = cmds.listConnections(obj_group, type="shadingEngine")
    if not shading_engines:
        return None
    shader = cmds.listConnections(shading_engines[0] + ".surfaceShader")[0]
    return shader

# haohao
# 检查生成的 MPD 文件是否正常，如果不正常则修复
# input: mpd_original 文件夹下的所有 MPD 文件
# output: mpd_fixed 文件夹

import os
import xml.etree.ElementTree as ET

# 注册命名空间，以避免保存文件时添加 ns0: 前缀
ET.register_namespace('', "urn:mpeg:dash:schema:mpd:2011")

def check_and_fix_mpd(file_path):
    file_name = os.path.basename(file_path)
    tree = ET.parse(file_path)
    root = tree.getroot()

    # 命名空间
    namespace = {"ns": "urn:mpeg:dash:schema:mpd:2011"}

    # 获取所有 AdaptationSet 标签
    adaptation_sets = root.findall("ns:Period/ns:AdaptationSet", namespaces=namespace)
    
    if len(adaptation_sets) <= 2:
        return  # 如果只有两个或更少 AdaptationSet 标签，则文件正常

    # 找到第一个视频 AdaptationSet 和音频 AdaptationSet
    main_video_adaptation_set = None
    audio_adaptation_set = None
    for aset in adaptation_sets:
        if aset.find("ns:Representation", namespaces=namespace).get("mimeType").startswith("video"):
            if main_video_adaptation_set is None:
                main_video_adaptation_set = aset
        elif aset.find("ns:Representation", namespaces=namespace).get("mimeType").startswith("audio"):
            audio_adaptation_set = aset

    # 合并所有视频 Representation 到第一个视频 AdaptationSet 中
    for aset in adaptation_sets:
        if aset is not main_video_adaptation_set and aset is not audio_adaptation_set:
            for representation in aset.findall("ns:Representation", namespaces=namespace):
                if representation.get("mimeType").startswith("video"):
                    main_video_adaptation_set.append(representation)
            root.find("ns:Period", namespaces=namespace).remove(aset)

    # 保存修改后的MPD文件
    out_path = os.path.join("mpd_fixed", file_name)
    print(out_path)
    # tree.write(out_path, encoding="utf-8", xml_declaration=True)
    tree.write(out_path, xml_declaration=True)

def main():
    for file_name in os.listdir("./mpd_original"):
        if file_name.endswith(".mpd"):
            print(f"Checking and fixing {file_name}...")
            file_path = os.path.join("./mpd_original", file_name)
            check_and_fix_mpd(file_path)
            print(f"{file_name} fixed if it was abnormal.")

if __name__ == "__main__":
    main()

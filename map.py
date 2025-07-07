import re
import json

# 读取lua文件内容
def read_lua_names(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # 用正则提取所有路径和name
    # 例如: b_abandoned={ name="Abandoned Deck", ... }
    # 支持多级路径
    pattern = re.compile(r'(\w+)\s*=\s*{([^{}]*?name\s*=\s*"([^"]+)")', re.DOTALL)
    # 递归提取所有name字段
    def extract_names(s, prefix=""):
        names = {}
        # 匹配当前层级的所有key
        for m in re.finditer(r'(\w+)\s*=\s*{', s):
            key = m.group(1)
            start = m.end()
            # 找到对应的闭合大括号
            count = 1
            i = start
            while i < len(s) and count > 0:
                if s[i] == '{':
                    count += 1
                elif s[i] == '}':
                    count -= 1
                i += 1
            block = s[start:i-1]
            # 查找name字段
            name_match = re.search(r'name\s*=\s*"([^"]+)"', block)
            if name_match:
                path = prefix + key
                names[path] = name_match.group(1)
            # 递归查找子结构
            sub_names = extract_names(block, prefix + key + ".")
            names.update(sub_names)
        return names
    return extract_names(content)

# 提取英文和中文name
names_en = read_lua_names('en-us.lua')
names_zh = read_lua_names('zh_CN.lua')

# 生成映射表
mapping = {}
for path, en_name in names_en.items():
    zh_name = names_zh.get(path)
    if zh_name:
        mapping[en_name] = zh_name

# 输出到json文件
with open('name_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)

print(f"已生成 {len(mapping)} 条中英文name映射，输出到 name_mapping.json")

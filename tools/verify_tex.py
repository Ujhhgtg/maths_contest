import re

text = open("论文正文.tex", "r", encoding="utf-8").read()

# 1. Brace balance
o, c = text.count("{"), text.count("}")
status = "OK" if o == c else "FAIL"
print(f"1. Braces: {o} = {c} -> {status}")

# 2. Math environment balance
for env in ["align*", "equation*", "align", "equation"]:
    for m in re.finditer(r"\\begin\{(" + env + r")\}", text):
        name = m.group(1)
        b = text.count("\\begin{" + name + "}")
        e = text.count("\\end{" + name + "}")
        if b != e:
            print(f"   UNBALANCED: {name} ({b} vs {e})")

# 3. Check \text{} subscripts
subs = re.findall(r"\\text\{([^}]+)\}", text)
suspect = []
for s in set(subs):
    has_chinese = any(ord(c) > 0x4E00 for c in s)
    is_unit = s in [
        "m",
        "kN",
        "MPa",
        "kg",
        "t",
        "s",
        "Pa",
        "mm",
        "m^2",
        "kN/m^2",
        "kN/m",
        "kN·m",
        "Ek",
        "^2",
        "kg/m",
    ]
    is_math_op = s in [""]
    if not (has_chinese or is_unit or is_math_op):
        suspect.append(s)

if suspect:
    print(f"2. SUSPICIOUS \\text subscripts: {suspect}")
else:
    print(f"2. All {len(set(subs))} unique \\text subscripts are valid")

# 4. Display math balance
opens = text.count(r"\[")
closes = text.count(r"\]")
print(
    f"3. Display math: [{opens} opens, {closes} closes] -> {'OK' if opens == closes else 'FAIL'}"
)

# 5. Check \begin/\end balance
for env in ["table", "figure", "tabular", "align*", "align", "itemize", "enumerate"]:
    b = text.count("\\begin{" + env + "}")
    e = text.count("\\end{" + env + "}")
    if b != e:
        print(f"   UNBALANCED: {env} ({b} vs {e})")

print("4. Verification complete.")

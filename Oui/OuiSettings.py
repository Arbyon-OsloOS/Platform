from OPlatform.SettingsAPI import Settings

accent = "#0075db"

#    light theme, dark theme
c_B = [  "#ffffff", "#282828"  ]
c_S = ["#eedddddd", "#ee373737"]
c_F = [  "#000000", "#ffffff"  ]
c_A = [  "#bbbbbb", "#323232"  ]
c_P = [  "#999999", "#424242"  ]
c_C = [  "#000000", "#ffffff"  ]
uiSettings = Settings("com.arbyon.ui")
if uiSettings.get("accent") is None:
    uiSettings.set("accent", accent)
else:
    accent = uiSettings.get("accent")

if uiSettings.get("dark") is None:
    uiSettings.set("dark", True)
    dark = True
else:
    dark = uiSettings.get("dark")

if uiSettings.get("accentDark") is None:
    accentDark = True
else:
    accentDark = uiSettings.get("accentDark")

lscache = [accent, dark, accentDark]

p_B = c_B[int(dark)]
p_S = c_S[int(dark)]
p_F = c_F[int(dark)]
p_A = c_A[int(dark)]
p_P = c_P[int(dark)]
p_C = c_C[int(accentDark)]

def pss(s):
    return s.replace("ACCENT", accent).replace(":A", p_A).replace(":B", p_B
    ).replace(":S", p_S).replace(":F", p_F).replace(":P", p_P).replace(":C",
    p_C)

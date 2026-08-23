# 双抗错配、半抗体与同源二聚体：杂质究竟从哪里来？

- 原文链接：https://mp.weixin.qq.com/s/d1Uu6RjBO1U2LQR5VdFjRg
- 公众号：云端悟道
- 发布时间：2026-08-23
- 剪藏时间：2026-08-23 17:10

---

第四季 · 双抗 | 004

[图片]

图 1 目标双抗与主要装配相关杂质的三维蛋白示意。结构域尺度参考完整 IgG 晶体结构（ PDB 1IGT/1HZH ）； AI 生成后由代码叠加标签，仅用于机制解释，不代表某一候选分子的原子坐标。

一句话结论｜ 双抗杂质不是在纯化车间 “ 突然出现 ” 的，它们大多在序列设计、链配对、细胞表达和分子应激阶段已经形成；下游真正能做的是识别并放大目标与杂质之间的微小差异。

导读： SEC 主峰，不等于正确装配

一个双抗样品可以在 SEC 上显示 98% 以上单体，却仍含有几乎等分子量的 knob-knob 、 hole-hole 或轻链错配体。它们可能保留完整 Fc 、拥有近似流体力学半径，甚至在常规 CE-SDS 中与主品接近；真正暴露问题的往往是非还原 / 亚基 LC-MS 、特异肽图、分析 HIC 、 IEX/icIEF 和双靶点功能测定。 [3-14,25-37]

因此，本期不从树脂目录出发，而沿 “ 分子结构 — 形成机制 —CQA— 分析身份 — 可分离差异 — 制造路线 ” 推进。读者既可以把它当作双抗入门产品画像，也可以直接用其中的条件窗口、方法组合和路线决策表搭建早期 DSP 开发方案。

14 ｜对象与结构：先把双抗分成六类

双特异抗体不是单一分子类型。按是否保留完整 Fc ，可分为 IgG 样与无 Fc 片段型；按对称性，可分为对称融合与不对称异源二聚；按价数，又可分为 1+1 、 2+1 、 2+2 以及更高价多特异格式。分类的价值不在命名，而在于它预示哪一种装配错误最可能成为 CQA 。经典不对称 IgG 若同时表达两条不同重链和两条不同轻链，理论上可形成 16 种 H2L2 链组合，对应 10 种不同抗体；只有两种排列代表期望双抗，未进行配对工程时理论上限仅 12.5% 。 [2-10]

结构类别

典型工程

优先杂质画像

建议起始路线

IgG样1+1

KiH 、静电导向、 SEED 、共同轻链

HC 同源二聚、半抗；共同轻链不能解决 HC 错配

Protein A→IEX/MMC→AEX

CrossMAb/正交Fab

结构域交叉或正交界面

LC 错配下降；可能出现缺链、交换衍生物

Protein A→MMC/IEX→AEX

κλ-body

两臂分别使用 κ 与 λ 轻链

亲本单特异体、 LC 相关副产物

Protein A→κ/λ差异亲和→IEX

IgG-scFv / 2+1

Fc上融合额外scFv/Fab

剪切、聚集、高黏度、低pH敏感

Protein A→HIC/CHT/MMC→AEX

DVD-Ig / 2+2

串联可变域与连接肽

局部疏水暴露、错误二硫键、片段

Protein A→HIC/MMC→AEX

BiTE/DART/TandAb/VHH

无完整 Fc 的小型多结构域分子

未装配链、截短体、过滤损失

Protein L/特异亲和→IEX/MMC/HIC

[图片]

图 2 分子格式与杂质风险的半定量映射。评分用于开发优先级，不是法规限度；最终以候选分子实测为准。

作用机制也会反向定义质量标准

T 细胞衔接器需要同时抓住 CD3 与肿瘤抗原，任何单臂错配都可能降低免疫突触形成；双通路阻断分子要求两臂保持正确亲和力和空间构象；受体聚簇、条件激活或血脑屏障穿梭分子还可能依赖价态、臂间距和顺序结合。由此，轻链错配即使不改变 SEC 纯度，也可能直接损伤效价或安全窗。 CQA 不能停留在 “ 单体、纯度、电荷 ” ，必须包括正确链组合、双靶点同时结合、 Fc 功能以及与机制相关的细胞效价。 [10-12]

15 ｜关键矛盾：这些杂质到底从哪里来

[图片]

图 3 从形成机制到 CQA ，再到可利用分离差异的翻译链。

半抗体通常只包含一条重链和一条轻链，约为完整 IgG 的一半；它可能保留一个 Fc 半部，因此仍能弱结合 Protein A 。 3/4 抗体或轻链缺失体的质量只比目标少一条轻链，常与主峰高度重叠。 knob-knob 和 hole-hole 同源二聚体在完整质量上几乎等同目标双抗， SEC 无法可靠区分，必须依赖非还原 SDS-PAGE 、还原 / 非还原 CE-SDS 、 HIC 或质谱。轻链错配体更棘手：分子量几乎不变，甚至常规肽图也需要选取特异肽段才能定量，但其双靶点结合和效价可能显著下降。 [25-37]

聚集体要区分可逆寡聚、共价高聚体和低 pH 诱导聚集；片段要定位铰链剪切、 Fab 脱落、 scFv 连接肽断裂还是蛋白酶特异切割。工艺相关杂质仍包括 HCP 、残余 DNA 、 Protein A 配基、培养基组分、内毒素和病毒。建议在早期小试就建立 “ 物种 — 方法 — 定量限 ” 表： SEC-MALS 负责尺寸和绝对分子量； HIC 放大疏水差异； IEX/icIEF 看电荷； LC-MS/ 亚基质谱确认链组合；双抗原桥联或双靶点细胞法确认功能。没有身份清楚的杂质峰，任何 DoE 都只是把未知峰从一个分段推到另一个分段。 [30-43]

重链错配：异源二聚竞争不过同源二聚

两条不同重链的 CH3 界面若没有工程约束，会随机形成 AA 、 AB 和 BB 。 KiH 通过 “ 大侧链 knob” 与 “ 小侧链 hole” 互补提高 AB 概率；静电导向在两条链上设置互补电荷，既改善装配，也可能拉开 AA 、 AB 、 BB 的 pI ； SEED 和受控 Fab 臂交换则从界面或后表达交换路径解决问题。 [2,3,5,77-80] 但任何方法都不是零杂质：表达比失衡、链降解、二硫键形成不完全和翻译后修饰仍会把理论优势侵蚀掉。

轻链错配：质量几乎不变，功能却可能丢一半

两条轻链都能接近两条重链时，会产生正确、单侧错配与双侧错配。共同轻链把组合数降到最低； CrossMAb 用一侧 CH1-CL 或 VH-VL 交换制造正交性；正交 Fab 界面和工程二硫键进一步引导亲本配对。轻链错配体与目标的完整质量往往相同，因此必须用特异肽、亚基 MS 或双抗原桥联 / 细胞功能方法确认。仅凭 SEC 或总非还原 CE 纯度放行，存在把 “ 结构错误的单体 ” 算成主品的系统性风险。 [4,6-10,35-37]

半抗、 3/4 抗与片段：不是同一个概念

半抗体通常由一条重链和一条轻链组成，约为完整 IgG 一半； 3/4 抗体通常缺失一条轻链或一个 Fab 相关链；片段则可能来自铰链、连接肽或结构域剪切。三者在 Protein A 上的行为取决于保留的 Fc/CH1/ 轻链结合位点，不应简单按分子量归类。半抗可能只有一个 Fc 结合单元，亲合力弱于完整双抗；缺失轻链的 3/4 抗仍可带完整 Fc ，因此可能与主品共洗脱；剪切片段若保留 Fc ，也会进入 Protein A 池。 [13,25-33]

16 ｜制造路线：上游、原液、下游和制剂是一条连续因果链

上游的链表达比例、启动子强度、基因拷贝、培养温度、补料与细胞死亡水平决定装配底盘。收获澄清阶段的蛋白酶和长时间停留会继续放大片段； Protein A 低 pH 洗脱与病毒灭活可能诱发构象松动和聚集；高盐 HIC/MMC 池会把渗透压和 UF/DF 负担传递给后续；制剂端的 pH 、离子强度、表面活性剂和高浓度黏度又会改变储存期聚集与颗粒。因此， “ 纯化前后纯度 ” 必须与全过程质量平衡和强制降解相连。 [15-24,38-58]

对于 KiH+ 共同轻链、杂质以同源二聚为主的 IgG 样双抗，可从 Protein A 捕获 →CEX pH 梯度 →AEX 流穿开始；若 CEX 分不开，直接把第二步换成 MMC ，不必机械增加第四柱。对于 CrossMAb/WuXiBody 、轻链缺失和错配更突出者，可采用 Protein A→MMC→AEX 流穿，必要时用 HIC 或 CHT 替代 AEX 完成聚集体 / 片段控制。对于 IgG-scFv 、 2+1 或多价融合蛋白，聚集风险高，捕获后应尽早做低 pH 中和和 HIC/CHT 筛选，并把剪切片段作为关键质量属性。对于 κλ -body ，可用 Protein A 后串联 KappaSelect/LambdaFabSelect 等差异亲和，再用 IEX 或 AEX 完成工艺相关杂质清除。 [54-61,73-86]

四条案例路线 ——AC+AEX+CEX 、 AC+AEX+HIC 、 AC+MMC+CHT 、 AC+AEX+CHT—— 恰好反映了上述思想：真正变化的是第三种选择性。平台化应建立 “ 首选路线 + 触发条件 ” ： SEC 聚集体高于 3–5% 触发 HIC/CHT 筛选； CE-SDS 轻链缺失超过方法定量限触发 MMC/ 亲和位点筛选； icIEF 显示同源二聚 pI 差异大于约 0.3 时优先 IEX ；若所有常规维度重叠，再回到分子工程。阈值需要按产品风险和阶段调整，不能作为法规通用限度。 [19-24,62-86]

17 ｜开发启示：先建立能看见杂质的方法

方法

最擅长回答

不能独立回答

SEC-HPLC / SEC-MALS

聚集体、片段、绝对分子量

同质量错配体常共峰；不证明链组合

还原/非还原CE-SDS

缺链、半抗、片段、二硫键相关物种

同质量同迁移率物种可能重叠

icIEF / CEX-HPLC

pI 与电荷变体；同源二聚初筛

局部电荷差异未必映射到整体 pI

分析HIC

疏水暴露、hole-hole等近质量物种

需单独鉴定峰身份；非通用定量

完整/亚基LC-MS

链组合、质量、糖型与截短

异构错配可能需要特异肽图

肽图/特异肽PRM

LC 错配、序列确认、修饰定位

方法开发成本高，需标准品或响应校正

双抗原桥联/细胞效价

同时结合与机制相关功能

不能单独定位结构杂质

最低组合｜ 早期克隆 / 工艺筛选至少采用 SEC + 非还原 CE-SDS + icIEF/IEX + 完整 / 亚基 LC-MS ；对轻链错配和同源二聚，再增加物种特异质谱、分析 HIC 或功能性正交方法。

18 ｜双抗纯化策略总览：先设计，再分离

[图片]

图 4 亲和、离子交换、混合模式与 HIC 的正交选择性三维示意。 AI 生成机制图，用于说明吸附差异，不代表具体商业填料配基结构。

18.1 分子设计：最便宜的一根 “ 隐形色谱柱 ”

如果项目仍处于候选筛选阶段，应优先通过 KiH 、静电导向、共同轻链、 CrossMAb 、正交 Fab 界面或受控 Fab 臂交换降低错误装配。更进一步，可在远离 CDR 、 FcRn 和效应功能界面的表面引入温和电荷差异，使 AA 、 AB 、 BB 在 IEX 上有可放大的顺序；也可让一条重链的 Protein A 结合位点失活，使无结合、单价结合与双价结合三类物种在 Protein A 上形成亲合力梯度。设计目标不是追求理论上 “ 绝对无杂质 ” ，而是让剩余杂质至少在亲和、电荷、疏水或尺寸中的一个维度与主品不同。 [62-82]

18.2 Protein A ：从捕获升级为结构选择步骤

完整 Fc 的 IgG 样双抗通常优先 Protein A 捕获。上样多在中性 pH 、低到中等电导，洗涤阶段通过盐、精氨酸、醋酸盐、少量有机助剂或 pH 调整降低 HCP 和非特异吸附，随后在约 pH 3.0–3.8 洗脱。双抗分子更易低 pH 聚集，因此要缩短柱上和收集罐停留时间，预置中和液，并用在线混合控制局部极端 pH 。若半抗只有一个完整 Protein A 结合单元，结合亲合力较低，可尝试线性或阶梯 pH 洗脱，让半抗先出、完整双抗后出；但 Protein A 结构域特异性、 IgG 亚型和 Fc 工程会改变窗口，不能把某一树脂上的 pH 直接移植。 [44-53]

对于无 Fc 片段、 scFv 、 Fab 或 VHH 多抗， Protein A 可能完全失效。 Protein L 识别部分 κ 轻链可变区，可捕获 Fab 、 scFv 和部分半抗；当完整分子、 3/4 抗和半抗包含的 Protein L 结合位点数不同，分段洗脱可形成亲合力分辨。 2025 年一项不对称双抗片段去除研究用 Protein L 线性及阶梯 pH 优化，观察到 pH 5.5 段富集半抗 / 片段、 pH 5.0 段目标纯度最好、 pH 4.5 段聚集体和片段上升；其逻辑是多位点亲合力而非简单 “pH 越低洗得越干净 ” 。 CH1 特异亲和和 κ / λ 串联亲和对特定格式更具结构选择性，但树脂成本、配基泄漏和清洗验证需要纳入平台评估。 [54-61]

齐鲁 — 亲和纯化双抗 案例：原文条件与可以借鉴的边界

Wen 等在上海齐鲁药物研究中心的 4 个不对称双抗案例中， bsAb 3 使用 4.7 mL 预装 UniMab 50HC 柱，载量 38.6 g/L resin ，统一停留时间 5 min 。平衡液为 50 mM Tris-HAc 、 0.15 M NaCl 、 pH 7.4 （ 5 CV ）；上样后依次用平衡液 3 CV 、 50 mM Tris-HAc + 0.5 M L-Arg 、 pH 7.4 ，以及 50 mM acetate 、 pH 5.5 （ 3 CV ）洗涤；洗脱液为 50 mM acetate + 1% PEG 4000 ，在 pH 4.0 、 4.1 、 4.2 、 4.3 、 4.4 、 4.5 间比较，每个条件 5 CV ；随后用 0.1 M acetate 、 pH 3.0 剥离，并以 0.1 M NaOH 3 CV 清洗。 [30]

原图显示，随洗脱 pH 由 4.0 升至 4.5 ，非还原 CE 主峰约由 83% 升至 91% ， LMW 约由 12% 降至 8% ， HMW 亦有下降趋势（数值由图 2C 近似读取，非作者表格原始值）。作者将改善归因于 1% PEG 4000 介导的共溶剂排斥与 pH 共同提高片段 / 主品分辨率。该结论只能说明 “ 这个分子 + 这个树脂 + 这个 PEG/pH 窗口 ” 有效；转移时必须重新评估 PEG 残留、池体积、低 pH 暴露、病毒过滤与 UF/DF 负担。

[图片]

图 5 原文图 2C 节选： UniMab 50HC 洗脱 pH 对 bsAb 3 非还原 CE 主峰、 HMW 与 LMW 的影响。来源： Wen Y, et al., 2025 ， Figure 2C ， © 原作者 / 期刊；本文仅作学术评论与数据解读。

18.3 CEX 与 AEX ：把 pI 和局部电荷斑块兑现成窗口

CEX 在 pH 低于蛋白 pI 时结合，常用 NaCl 梯度或 pH 梯度洗脱； AEX 在 pH 高于 pI 时结合，也可用流穿模式让目标不结合、 DNA/HCP/ 病毒和部分聚集体留在柱上。双抗同源二聚体与目标异源二聚体如果具有 0.2–1 个 pI 单位差异， IEX 通常是最经济、最易放大的选择。工程上可在两条重链表面引入互补电荷对，既促进异二聚，也使 knob-knob 、目标和 hole-hole 沿梯度错开。共同轻链 IgG 样双抗已有高线性 pH 梯度纯化报道，其优势是 pH 梯度比盐梯度更直接映射 pI 差异，缺点是缓冲体系、柱体积和设备混合精度会影响重现性。 [62-67]

实际开发不要只筛 pH 和盐。树脂配基密度、孔径、上样载量、停留时间、蛋白浓度和温度都会改变局部吸附。应先用分析 IEX/icIEF 估计差异，再用 96 孔或微柱筛选 pH 4.5–9.0 、 0–500 mM NaCl ，区分结合 - 洗脱和流穿模式。若分子 pI 很高、主峰与同源二聚体重叠，可尝试 AEX 在较高 pH 下利用局部电荷斑块；若聚集体更强结合 CEX ，降低载量和选择合适洗涤盐度通常比无限拉长梯度更有利于放大。 IEX 的真正价值不是 “ 平台第二柱 ” ，而是把结构工程制造的电荷差异变成可控分段。 [63-72]

建议起始筛选范围｜ CEX/AEX 用分析 pI 定位后，先覆盖 pH 相对目标 pI 约 ±1.5 、 NaCl 0-500 mM ，并同时比较结合 - 洗脱与流穿模式。这里是开发起点，不是推荐工艺条件；树脂配基密度、孔径、载量、停留时间和缓冲离子必须进入 DoE 。

18.4 MMC ：当质量和 pI 都太接近

混合模式层析同时包含离子交换、疏水、芳香、氢键等作用，能够把单一维度上很小的差异叠加成可见选择性。 2020 年 KiH 双抗案例中， Capto MMC ImpRes 在优化洗涤和洗脱后，将含半抗、 hole-hole 同源二聚体和聚集体的上样纯度由 73.3% 提高到 99.0% ；研究同时用分析 HIC 监测几乎等质量的 hole-hole 物种，说明制备和分析选择性必须配套。 [73]

WuXiBody 双抗研究用同类 MMC 去除轻链缺失体与聚集体：两个分子的最优窗口并不相同，提示 “ 同平台同树脂 ” 仍需针对表面性质重做条件。 2026 年单柱多 pH MMC 方法更具启发性： pH 7.5 上样， pH 9.5 洗掉半抗和同源二聚；降至 pH 5.5 后用 1 M NaCl 去除轻链错配，最后 pH 8.0/1 M NaCl 回收目标，纯度从 67.3% 升至 94.5% ，总回收 72% 。同年另一项双 pH- 盐梯度方案使用 50 mM Tris-HCl 、 200 mM NaCl 、 pH 7.0 洗涤， 500–600 mM NaCl 、 pH 7.5 洗脱，将主要同源二聚体从 26.0–26.3% 降至 0.1–0.3% ，次要同源二聚体从 1.7–2.0% 降至 1.0–1.2% ，聚集体从 4.7–5.2% 降至 2.4–2.7% ，回收 62.9–64.1% 。这些案例证明 MMC 的强项是扩大窗口，代价则是条件空间大、清洗与生命周期验证更复杂。 [74-77]

18.5 HIC 、 CHT 与 SEC ：处理疏水面、片段和尺寸

HIC 在高盐下促进蛋白疏水面与配基结合，随盐浓度下降洗脱。双抗新增 scFv 、连接肽或错配界面后，局部疏水暴露常比主分子更强，因此 HIC 对聚集体、错配体和部分片段具有高分辨率。 2025 年 DAF 双抗研究显示，合理选择配基和盐梯度可显著去除聚集体；用户提供 PPT 中的放大案例也观察到淋洗段带走多数片段、主洗脱几乎不见片段。 HIC 缺点是高盐负担、样品预处理、设备腐蚀和废液量；若高浓度硫酸铵本身诱发聚集，可改用较温和盐、低配基密度或疏水性较弱填料。 [78-81]

羟基磷灰石（ CHT ）兼有阳离子交换与钙位点亲和，可同时响应蛋白表面羧基、磷酸基和电荷，常对片段、聚集体、核酸与 Protein A 浸出物显示正交选择性。公开和用户提供案例中，低分子片段可由 95.2% 提升到 98.1% 、回收约 89% ；聚集体加片段可由 94.4% 提升到 99.2% 、回收约 82.6% 。但 CHT 对磷酸盐浓度、 pH 、钙离子、清洗和柱床稳定更敏感，需要严格控制缓冲液配方。 SEC 分辨率直观、机制简单，却载量低、稀释大，适合分析、临床早期小批或最后救援，不宜默认作为商业规模抛光柱。 [80-86]

[图片]

图 6 文献与公开案例的步骤前后纯度及回收率。不同分子、上样组成和分析方法不可横向排名；图用于显示选择性 — 回收的权衡。 [26-34]

18.6 把树脂串成最短正交路线

[图片]

图 7 杂质驱动的双抗纯化路线选择。 AEX 流穿通常继续承担 HCP 、 DNA 和病毒清除，不应被迫承担所有产品相关杂质。

同源二聚体：先确认 pI 和 HIC 保留差异。差异明显时优先 CEX/AEX ；差异小但局部疏水不同，优先 MMC 或 HIC ；若分子设计尚可调整，增加表面电荷对比在下游堆叠更多树脂更经济。半抗和 3/4 抗：优先利用 Protein A 、 Protein L 、 CH1 或 κ 结合位点数差异做分段亲和；若与目标共洗脱，再用 MMC 或 CHT 。轻链缺失 / 错配：完整质量接近， SEC 通常无效；用亚基质谱确认后，筛 MMC 多 pH 、多盐策略，并以 HIC/IEX 作为正交候选。 [57-77]

聚集体和寡聚体：低聚体可先用 SEC-MALS 定量； AEX 流穿适合同时降 HCP/DNA 和部分聚集体， CEX 结合 - 洗脱、 HIC 、 MMC 、 CHT 均可作为精抛。片段与游离链：亲和位点数、尺寸和疏水性是三条主线； Protein L/CH1 亲和、 CHT 和 MMC 通常比 SEC 更能放大。 HCP 与 DNA ：不要因聚焦产品相关杂质而忽略平台清除， Protein A 强化洗涤、 AEX 流穿和病毒过滤仍是必要骨架。每次选择都要用 “ 杂质清除倍数、主品回收、载量、池体积、缓冲液复杂度、 CIP 稳定性 ” 六个指标共同评分。 [33-45,87-93]

产品画像

首选最短路线

触发调整

KiH+ 共同轻链；同源二聚为主

Protein A→CEX pH梯度→AEX流穿

若pI重叠，CEX替换为MMC；分析HIC确认hole-hole

CrossMAb/WuXiBody；缺链/LC错配

Protein A→MMC→AEX流穿

必要时以 HIC 或 CHT 替换末端抛光

IgG-scFv/2+1；聚集/剪切高

Protein A→HIC或CHT→AEX

捕获池快速中和；监控加盐诱导聚集

κλ-body

Protein A→Kappa/Lambda差异亲和→IEX

监控亲本单特异体与配基泄漏

无Fc片段多抗

Protein L/CH1/特异亲和→MMC/IEX→HIC

同步评估膜吸附、过滤回收和截短体

可直接执行的六周开发框架

第一周先做样品和方法准备。用 Protein A 池或培养上清建立完整质量、亚基质量、非还原 CE-SDS 、 SEC 和 icIEF 基线；每个主要峰至少收集一次并用 LC-MS 确认。将关键杂质分成装配错误、聚集 / 片段、工艺相关杂质三组。没有峰身份时，不要用 “ 前杂、后杂 ” 代替，因为同一个保留时间在条件改变后可能代表不同物种。准备多种缓冲体系覆盖 pH 5—9 ，并记录缓冲离子本身对 MMC 和 CHT 选择性的影响。所有筛选样品统一蛋白浓度和电导，避免把稀释效应误当成树脂选择性。

第二周做亲和与 IEX 初筛。 Protein A 使用中性上样，比较基础洗涤、高盐、精氨酸和轻度 pH 洗涤，再做 pH 6.0 到 3.2 线性洗脱，观察半抗、完整双抗和聚集体分段。 Protein L 或 CH1 亲和只对结构上存在相应位点的分子开展，先确认每个物种的理论结合位点数。 CEX 以 pH 低于目标 pI 约 0.5—1.5 为起点，比较 0—500 mM NaCl 梯度； AEX 同时考察结合 - 洗脱和流穿。每个条件至少用目标回收、关键错配残留、池体积三项响应；只看总 A280 回收，会把共洗脱杂质也算成产品。

第三周做 MMC 、 HIC 和 CHT 正交筛选。 MMC 至少采用 pH× 盐二维设计；对轻链错配和同源二聚同时存在的样品，可参考多 pH 步骤逻辑：中性上样、高 pH 洗除一组杂质、酸性条件重新分配结合，再以高盐回收。 HIC 从弱到中等疏水配基开始，比较盐种及起始浓度；如果加盐后样品浑浊或 SEC 聚集升高，应停止该条件。 CHT 以低磷酸盐起步，逐步增加磷酸盐或 NaCl ，避免含 EDTA 等螯合剂的样品直接上柱。实验同时记录柱压、峰对称性、拖尾、清洗恢复和再生后空白。

第四周进行小柱确认和路线收敛。把初筛前两名条件转到 1—5 mL 柱，使用与未来放大相近的停留时间，测试 50% 、 100% 和 150% 目标载量。分段收集峰前、峰中、峰后，建立关键杂质突破曲线。若高载量下分辨率突然崩溃，说明选择性依赖未饱和位点，商业操作载量必须留安全余量。路线比较采用加权评分：关键杂质清除、回收、 HCP/DNA/ 病毒贡献、池体积、缓冲液和废液、柱寿命与 CIP 、操作复杂度共同计分，避免仅凭一张漂亮色谱图选择昂贵而脆弱的路线。

第五周开展稳健性和放大风险研究。围绕选定条件故意改变 pH 、电导、载量、停留时间、上样浓度和温度，确认池切割仍满足要求。对低 pH 洗脱测定从洗脱到中和的真实暴露时间；对 HIC 测定加盐、等待和上柱三个阶段的聚集变化；对 MMC 验证柱内 pH 过渡；对 CHT 确认磷酸盐和清洗后钙磷析出风险。只有最差组合下仍具备回收和杂质余量，才能把条件写入工艺描述。

第六周把纯化与制剂及病毒安全连起来。高盐 MMC/HIC 池可能增加 UF/DF 负担并降低病毒过滤通量；低 pH 捕获池可能改变后续电荷分布； CHT 磷酸盐池可能不适合直接进入某些膜步骤。应在流程级计算质量平衡、体积、时间和缓冲液。一个纯度高 0.3 个百分点但回收低 10% 、池体积翻倍的步骤，通常不是更好的商业选择。最后形成杂质结构与分析清单、层析选择性与设计空间报告、全流程质量平衡三份文件，分别回答 “ 峰是什么 ”“ 为什么能分开 ”“ 能否稳定生产 ” 。

专利视角：四大法域都在保护 “ 可制造性 ”

[图片]

图 8 代表性专利族时间线。检索覆盖 WIPO 、美国、欧洲、中国与日本公开文本；同族号合并展示，不代表法律状态意见。

专利的共同趋势非常清楚：第一代保护重链异源二聚界面（US5731168A）；随后把pI工程、结构域交叉、Fab臂交换和正交界面写入装配策略；再往后直接保护“为纯化而设计”的Fc/Protein A亲和差异、KappaSelect/CH1选择性以及AEX+MMC流程组合。 对研发团队而言，自由实施分析不应只查靶点与 CDR ，还应同时覆盖链配对突变、亲和位点失活、 pI 改造与专用纯化步骤。 [62-82]

本文列出的专利仅用于技术脉络，不构成法律意见。进入候选锁定和工艺定版前，应按国家 / 地区核对同族、权利要求、法律状态、到期日及许可范围；中国、美国、欧洲和日本同族的权利要求可能并不完全相同。

结 语：真正的双抗平台，是从结构读出工艺

双抗纯化的核心不是找到 “ 最强 ” 的填料，而是让目标与杂质在至少一个可放大的维度上不同。 Protein A/L 和 CH1 亲和放大结合位点数； IEX 放大 pI 和电荷斑块； MMC 叠加电荷、疏水和氢键； HIC 识别疏水暴露； CHT 提供不同于有机聚合物的表面化学。只要先把每种杂质的结构身份、形成原因和表面性质说清楚，路线就不再是盲筛。 [1-24,44-86]

产业化判断应遵循三个原则：第一，用分子工程减少杂质并制造可分离性，通常比增加一根商业规模柱更便宜；第二，用至少两种正交分析方法确认关键错配，不被 “ 总纯度 ” 迷惑；第三，以回收率、池体积、缓冲液成本、 CIP 寿命和最差条件稳健性共同评价工艺。双抗越复杂，越需要简单而有机制的下游流程。真正的平台不是一张固定流程图，而是一套能够从结构读出纯化路线的能力。

给项目团队的三个问题｜ ① 主峰里是否还藏着结构错误但质量相同的分子？ ② 每个关键杂质至少有两种正交方法能确认吗？ ③ 当前路线放大的是哪一种物理化学差异，若差异消失，是否该回到序列设计？

附录 A ｜杂质 — 分析 — 纯化决策速查

杂质

身份方法

优先制备手段

核心差异

半抗/3/4抗

nrCE-SDS、亚基MS

Protein A/L分段；CH1；MMC

亲和位点数/质量

AA/BB同源二聚

分析HIC、IEX、原生MS

CEX/AEX；MMC；HIC

pI/局部疏水/亲和

轻链缺失

亚基MS、CE-SDS

MMC；CH1/κ亲和；CHT

位点数/局部电荷

轻链错配

特异肽 LC-MS 、双靶点效价

多pH MMC；IEX/HIC

局部电荷/疏水

聚集体

SEC-MALS、AUC

HIC；AEX；MMC；CHT

尺寸/疏水暴露

剪切片段

CE-SDS、LC-MS

亲和分段；CHT；MMC

尺寸/保留位点

HCP/DNA/病毒

ELISA/LC-MS、qPCR、病毒验证

Protein A强化洗涤；AEX；病毒过滤

电荷/非特异结合/尺寸

附录 B ｜参考文献、专利与监管资料

采用 Vancouver 顺序编号。以同行评议论文、专利原文、 PDB 和监管指南为主；供应商应用资料与内部交流资料未作为关键结论证据。

Nisonoff A, Wissler FC, Lipman LN. Properties of      the major component of a peptic digest of rabbit antibody. Science.      1960;132(3441):1770-1771. doi:10.1126/science.132.3441.1770.      PMID:13729245.

Ridgway JB, Presta LG, Carter P.      ‘Knobs-into-holes’ engineering of antibody CH3 domains for heavy chain      heterodimerization. "Protein Engineering, Design and Selection".      1996;9(7):617-621. doi:10.1093/protein/9.7.617.

Merchant AM, Zhu Z, Yuan JQ, Goddard A, Adams CW,      Presta LG, et al. An efficient route to human bispecific IgG. Nature      Biotechnology. 1998;16(7):677-681. doi:10.1038/nbt0798-677.

Schaefer W, Regula JT, Bähner M, Schanzer J,      Croasdale R, Dürr H, et al. Immunoglobulin domain crossover as a generic      approach for the production of bispecific IgG antibodies. Proceedings of      the National Academy of Sciences. 2011;108(27):11187-11192.      doi:10.1073/pnas.1019002108.

Labrijn AF, Meesters JI, de Goeij BECG, van den      Bremer ETJ, Neijssen J, van Kampen MD, et al. Efficient generation of      stable bispecific IgG1 by controlled Fab-arm exchange. Proceedings of the      National Academy of Sciences. 2013;110(13):5145-5150.      doi:10.1073/pnas.1220145110.

Lewis SM, Wu X, Pustilnik A, Sereno A, Huang F,      Rick HL, et al. Generation of bispecific IgG antibodies by structure-based      design of an orthogonal Fab interface. Nature Biotechnology.      2014;32(2):191-198. doi:10.1038/nbt.2797.

Fischer N, Elson G, Magistrelli G, Dheilly E,      Fouque N, Laurendon A, et al. Exploiting light chains for the scalable      generation and platform purification of native human bispecific IgG.      Nature Communications. 2015;6(1):6113. doi:10.1038/ncomms7113.

Klein C, Schaefer W, Regula JT. The use of      CrossMAb technology for the generation of bi- and multispecific      antibodies. mAbs. 2016;8(6):1010-1020. doi:10.1080/19420862.2016.1197457.

Brinkmann U, Kontermann RE. The making of      bispecific antibodies. mAbs. 2017;9(2):182-212.      doi:10.1080/19420862.2016.1268307.

Labrijn AF, Janmaat ML, Reichert JM, Parren PWHI.      Bispecific antibodies: a mechanistic review of the pipeline. Nature      Reviews Drug Discovery. 2019;18(8):585-608. doi:10.1038/s41573-019-0028-1.

Spiess C, Zhai Q, Carter PJ. Alternative      molecular formats and therapeutic applications for bispecific antibodies.      Molecular Immunology. 2015;67(2):95-106. doi:10.1016/j.molimm.2015.01.003.

Amash A, Volkers G, Farber P, Griffin D, Davison      KS, Goodman A, et al. Developability considerations for bispecific and      multispecific antibodies. mAbs. 2024;16(1):2394229.      doi:10.1080/19420862.2024.2394229.

Li Y. A brief introduction of IgG-like bispecific      antibody purification: Methods for removing product-related impurities.      Protein Expression and Purification. 2019;155:112-119.      doi:10.1016/j.pep.2018.11.011.

Giese G, Williams A, Rodriguez M, Persson J.      Bispecific antibody process development: Assembly and purification of knob      and hole bispecific antibodies. Biotechnology Progress.      2018;34(2):397-404. doi:10.1002/btpr.2590.

Hober S, Nord K, Linhult M. Protein A      chromatography for antibody purification. Journal of Chromatography B.      2007;848(1):40-47. doi:10.1016/j.jchromb.2006.09.030.

Shukla AA, Thömmes J. Recent advances in      large-scale production of monoclonal antibodies and related proteins.      Trends in Biotechnology. 2010;28(5):253-261.      doi:10.1016/j.tibtech.2010.02.001.

Liu HF, Ma J, Winter C, Bayer R. Recovery and      purification process development for monoclonal antibody production. mAbs.      2010;2(5):480-499. doi:10.4161/mabs.2.5.12645.

Kelley B. Industrialization of mAb production      technology: The bioprocessing industry at a crossroads. mAbs. 2009;1(5):443-452.      doi:10.4161/mabs.1.5.9448.

Shukla AA, Hubbard B, Tressel T, Guhan S, Low D.      Downstream processing of monoclonal antibodies—Application of platform      approaches. Journal of Chromatography B. 2007;848(1):28-39.      doi:10.1016/j.jchromb.2006.09.026.

Fahrner RL, Knudsen HL, Basey CD, et al.      Industrial purification of pharmaceutical antibodies: development,      operation, and validation of chromatography processes. Biotechnol Genet      Eng Rev. 2001;18:301-327. PMID:11530694.

Carta G, Jungbauer A. Protein Chromatography:      Process Development and Scale-Up. Wiley-VCH; 2010.

Gottschalk U. Bioseparation in Antibody      Manufacturing. Wiley; 2008.

Shukla AA, Norman C. Process Scale Purification      of Antibodies. Wiley; 2009.

Gagnon P. Purification Tools for Monoclonal Antibodies.      Validated Biosystems; 1996.

Chen T, Han J, Guo G, Wang Q, Wang Y, Li Y.      Monitoring removal of hole-hole homodimer by analytical hydrophobic      interaction chromatography in purifying a bispecific antibody. Protein      Expression and Purification. 2019;164:105457.      doi:10.1016/j.pep.2019.105457.

Tang J, Zhang X, Chen T, Wang Y, Li Y. Removal of      half antibody, hole-hole homodimer and aggregates during bispecific      antibody purification using MMC ImpRes mixed-mode chromatography. Protein      Expression and Purification. 2020;167:105529.      doi:10.1016/j.pep.2019.105529.

Wan Y, Zhang T, Wang Y, Wang Y, Li Y. Removing      light chain-missing byproducts and aggregates by Capto MMC ImpRes      mixed-mode chromatography during the purification of two WuXiBody-based      bispecific antibodies. Protein Expression and Purification.      2020;175:105712. doi:10.1016/j.pep.2020.105712.

DiSpirito C, Parasnavis S, Aspelund M, Cramer SM.      A single column multimodal cation exchange process for removal of half      antibody, homodimer and light chain mispaired product-related impurities      from a bispecific antibody. Journal of Chromatography A. 2026;1771:466745.      doi:10.1016/j.chroma.2026.466745.

Li Q, Qin G, Zhao H, Liang X, Wang Z, He Q, et      al. Removal of homodimers of bispecific antibody via mixed-mode chromatography      with dual pH-salt gradients. Protein Expression and Purification.      2026;241:106932. doi:10.1016/j.pep.2026.106932.

Wen Y, Ye Y, Wang Z, Xu J, Meng Z, Luo W, et al.      Removal of Antibody-Related Fragments During Asymmetric Bispecific      Antibody Purification. Asian Journal of Complementary and Alternative      Medicine. 2025;13(1). doi:10.53043/2347-3894.acam13002.

Zhao P, Qi Y, Gao K. Removal of Aggregates During      Bispecific Antibody Purification Using Hydrophobic Interaction      Chromatography. Membranes. 2025;15(10):299. doi:10.3390/membranes15100299.

O’Connor E, Aspelund M, Bartnik F, Berge M,      Coughlin K, Kambarami M, et al. Monoclonal antibody fragment removal      mediated by mixed mode resins. Journal of Chromatography A.      2017;1499:65-77. doi:10.1016/j.chroma.2017.03.063.

Toueille M, Uzel A, Depoisier JF, Gantier R.      Designing new monoclonal antibody purification processes using mixed-mode      chromatography sorbents. Journal of Chromatography B.      2011;879(13-14):836-843. doi:10.1016/j.jchromb.2011.02.047.

Gagnon P, Ng P, Zhen J, et al. Monoclonal      antibody purification with hydroxyapatite. New Biotechnol.      2009;25(5):287-293. doi:10.1016/j.nbt.2009.03.017.

Yan Y, Xing T, Wang S, Daly TJ, Li N. Coupling      Mixed-Mode Size Exclusion Chromatography with Native Mass Spectrometry for      Sensitive Detection and Quantitation of Homodimer Impurities in Bispecific      IgG. Analytical Chemistry. 2019;91(17):11417-11424.      doi:10.1021/acs.analchem.9b02793.

Sharkey B, Pudi S, Wallace Moyer I, Zhong L,      Prinz B, Baruah H, et al. Purification of common light chain IgG-like      bispecific antibodies using highly linear pH gradients. mAbs.      2017;9(2):257-268. doi:10.1080/19420862.2016.1267090.

Dong W, Li Y. CH1-specific affinity resins      possess the potential of separating heterodimer from homodimers in asymmetric      bispecific antibody purification. Journal of Biological Methods.      2024;11(3):e99010020. doi:10.14440/jbm.2024.0026.

Levy NE, Valente KN, Lee KH, Lenhoff AM. Host      cell protein impurities in chromatographic polishing steps for monoclonal      antibody purification. Biotechnology and Bioengineering.      2016;113(6):1260-1272. doi:10.1002/bit.25882.

Tait A, Hogwood C, Smales C, Bracewell D. Host      cell protein dynamics in the supernatant of a mAb producing CHO cell line.      Biotechnology and Bioengineering. 2012;109(4):971-982.      doi:10.1002/bit.24383.

Tarrant RDR, Velez-Suberbie ML, Tait AS, Smales      CM, Bracewell DG. Host cell protein adsorption characteristics during      protein A chromatography. Biotechnol Prog. 2012;28(4):1037-1044.      doi:10.1002/btpr.1581.

Yigzaw Y, Piper R, Tran M, Shukla A. Exploitation      of the Adsorptive Properties of Depth Filters for Host Cell Protein      Removal during Monoclonal Antibody Purification. Biotechnology Progress.      2006;22(1):288-296. doi:10.1021/bp050274w.

Tugcu N, Roush DJ, Göklen KE. Maximizing      productivity of chromatography steps for purification of monoclonal      antibodies. Biotechnology and Bioengineering. 2008;99(3):599-613.      doi:10.1002/bit.21604.

Shukla AA, Hinckley P. Host cell protein      clearance during protein a chromatography: Development of an improved      column wash step. Biotechnology Progress. 2008;24(5):1115-1121.      doi:10.1002/btpr.50.

Tsumoto K, Umetsu M, Kumagai I, Ejima D, Philo J,      Arakawa T. Role of Arginine in Protein Refolding, Solubilization, and      Purification. Biotechnology Progress. 2004;20(5):1301-1308.      doi:10.1021/bp0498793.

Ghose S, Allen M, Hubbard B, Brooks C, Cramer SM.      Antibody variable region interactions with Protein A: Implications for the      development of generic purification processes. Biotechnology and Bioengineering.      2005;92(6):665-673. doi:10.1002/bit.20729.

Follman DK, Fahrner RL. Factorial screening of      antibody purification processes using three chromatography steps without      protein A. Journal of Chromatography A. 2004;1024(1-2):79-85.      doi:10.1016/j.chroma.2003.10.060.

Fussl F, Trappe A, Carillo S, Jakes C, Bones J.      Monoclonal antibody charge variant characterization by fully automated      four-dimensional liquid chromatography–mass spectrometry. J Chromatogr A.      2021;1653:462409. doi:10.1016/j.chroma.2021.462409.

Harinarayan C, Mueller J, Ljunglöf A, Fahrner R,      Van Alstine J. An exclusion mechanism in ion exchange chromatography.      Biotechnol Bioeng. 2006;95(5):775-787. doi:10.1002/bit.21029.

Fekete S, Beck A, Veuthey JL, Guillarme D. Theory      and practice of size exclusion chromatography for the analysis of protein      aggregates. J Pharm Biomed Anal. 2014;101:161-173.      doi:10.1016/j.jpba.2014.04.011.

Wu D, Wang Y, Lin DQ, Yao SJ. Evaluation of a new      mixed-mode resin for antibody purification. J Chromatogr A. 2016;1429:258-264.      doi:10.1016/j.chroma.2015.12.047.

Zhang S, Wan Y, Duan J, Li Y. Evaluating a new      mixed-mode resin Diamond MMC Mustang using Capto MMC ImpRes as a      benchmark. Protein Expression and Purification. 2021;186:105930.      doi:10.1016/j.pep.2021.105930.

Pezzini J, Joucla G, Gantier R, Toueille M,      Lomenech AM, Le Sénéchal C, et al. Antibody capture by mixed-mode      chromatography: A comprehensive study from determination of optimal      purification conditions to identification of contaminating host cell      proteins. Journal of Chromatography A. 2011;1218(45):8197-8208.      doi:10.1016/j.chroma.2011.09.036.

Gagnon P. Dissociation of Antibody–Contaminant      Complexes With Hydroxyapatite. BioProcessing Journal. 2011;9(2):14-24.      doi:10.12665/j92.gagnon.

Gagnon P. Improved antibody aggregate removal by      hydroxyapatite chromatography in the presence of polyethylene glycol.      Journal of Immunological Methods. 2008;336(2):222-228.      doi:10.1016/j.jim.2008.05.002.

Hou Y, Cramer SM. Competitive binding of      monoclonal antibody monomer-dimer mixtures on ceramic hydroxyapatite. J      Chromatogr A. 2019;1587:136-145. doi:10.1016/j.chroma.2018.12.023.

Chen J, Tetrault J, Ley A. Comparison of standard      and new generation hydrophobic interaction chromatography resins in the      monoclonal antibody purification process. Journal of Chromatography A.      2008;1177(2):272-281. doi:10.1016/j.chroma.2007.07.083.

Chen X, Wang Y, Li Y. Removing half antibody      byproduct by Protein A chromatography during purification of a bispecific      antibody. Protein Expr Purif. 2020;172:105635.      doi:10.1016/j.pep.2020.105635. PMID:32268171.

Beyer B, Jungbauer A. Conformational changes of      antibodies upon adsorption onto hydrophobic interaction chromatography      surfaces. Journal of Chromatography A. 2018;1552:60-66.      doi:10.1016/j.chroma.2018.04.009.

Aumann L, Morbidelli M. A continuous multicolumn      countercurrent solvent gradient purification (MCSGP) process.      Biotechnology and Bioengineering. 2007;98(5):1043-1055.      doi:10.1002/bit.21527.

Aumann L, Ströhlein G, Morbidelli M.      Chromatographic separation of three monoclonal antibody variants using      multicolumn countercurrent solvent gradient purification (MCSGP).      Biotechnol Bioeng. 2008;100(6):1166-1177. doi:10.1002/bit.21843.

Klutz S, Magnus J, Lobedann M, Schwan P, Maiser      B, Niklas J, et al. Developing the biofacility of the future based on      continuous processing and single-use technology. Journal of Biotechnology.      2015;213:120-130. doi:10.1016/j.jbiotec.2015.06.388.

US5731168A. Method for making heteromultimeric      polypeptides (knobs-into-holes). Patent document.

WO2009080251A1. Bispecific antibodies with      immunoglobulin domain crossover. Patent document.

WO2011131746A1. Bispecific antibodies by      controlled Fab-arm exchange. Patent document.

EP3268390B1. Methods of purifying bispecific      antibodies. Patent document.

US10934344B2. Methods of modifying antibodies for      purification of bispecific antibodies. Patent document.

EP2009101B1 / JP5144499B2. Purification based on      engineered isoelectric-point differences. Patent document.

WO2007114325A1. Methods of modifying antibodies      for purification. Patent document.

US20120039904A1. Dual-affinity re-targeting      proteins. Patent document.

US20090060910A1. Dual-variable-domain      immunoglobulins. Patent document.

US12343702B2. Anion-exchange hydrophobic mixed-mode      chromatography resin. Patent document.

EP2782925B1. Protein purification using Bis-Tris      buffer and multimodal resin. Patent document.

JP6335785B2. Mixed-mode antibody affinity      separation matrix. Patent document.

CN105177091A. Antibody modification and      purification based on pI difference. Patent document.

CN111356477B / JP7685771B2 / EP3661555B1.      Bispecific antibodies and uses thereof. Patent document.

WO2019028125A1. Bispecific antibody family and      production methods. Patent document.

Gunasekaran K, Pentony M, Shen M, Garrett L,      Forte C, Woodward A, et al. Enhancing Antibody Fc Heterodimer Formation      through Electrostatic Steering Effects. Journal of Biological Chemistry.      2010;285(25):19637-19646. doi:10.1074/jbc.m110.117382.

Davis JH, Aperlo C, Li Y, Kurosawa E, Lan Y, Lo      KM, et al. SEEDbodies: fusion proteins based on strand-exchange engineered      domain (SEED) CH3 heterodimers in an Fc analogue platform for asymmetric      binders or immunofusions and bispecific antibodies†. Protein Engineering,      Design and Selection. 2010;23(4):195-202. doi:10.1093/protein/gzp094.

Strop P, Ho WH, Boustany LM, Abdiche YN,      Lindquist KC, Farias SE, et al. Generating Bispecific Human IgG1 and IgG2      Antibodies from Any Antibody Pair. Journal of Molecular Biology.      2012;420(3):204-219. doi:10.1016/j.jmb.2012.04.020.

Sampei Z, Igawa T, Soeda T, Okuyama-Nishida Y,      Moriyama C, Wakabayashi T, et al. Identification and Multidimensional      Optimization of an Asymmetric Bispecific IgG Antibody Mimicking the      Function of Factor VIII Cofactor Activity. PLoS ONE. 2013;8(2):e57479.      doi:10.1371/journal.pone.0057479.

WO2012162068A1. Bispecific antibodies having      engineered orthogonal Fab interfaces. Patent document.

WO2014110222A1. Bispecific antibodies with common      light chains and purification-compatible formats. Patent document.

ICH Q6B. Specifications: Test Procedures and      Acceptance Criteria for Biotechnological/Biological Products.

ICH Q5A(R2). Viral Safety Evaluation of      Biotechnology Products Derived from Cell Lines.

ICH Q5C. Stability Testing of      Biotechnological/Biological Products.

ICH Q8(R2). Pharmaceutical Development.

ICH Q9(R1). Quality Risk Management.

ICH Q11. Development and Manufacture of Drug      Substances.

FDA. Development of Therapeutic Protein      Biosimilars: Comparative Analytical Assessment; 2019.

EMA. Guideline on Development, Production,      Characterisation and Specifications for Monoclonal Antibodies; 2009.

RCSB PDB 1IGT. Refined structure of intact IgG2a      monoclonal antibody.

RCSB PDB 1HZH. Crystal structure of intact human      IgG1 b12.

RCSB PDB 6WVZ. Anti-MET Fab arm of amivantamab in      complex with human MET.

RCSB PDB 6T9E. Bispecific DutaFab complex.

Li Y. General strategies for IgG-like bispecific      antibody purification. Biotechnol Prog. 2025;41(2):e3515.      doi:10.1002/btpr.3515. PMID:39410750.

WO2016018740A2 / EP3172221B1. Purification      platform for bispecific antibodies using engineered Protein A-binding      avidity and chaotropic modifiers. Patent family.

WO2021170060A1. Purification of bispecific      antibodies by KappaSelect affinity chromatography. Patent document.

US20210355215A1. Methods for purifying      heterodimeric, multispecific antibodies using engineered pI differences.      Patent document.

CN115734969A / WO2021208839A1. Purification of      bispecific antibodies using Protein A, bind-elute AEX and mixed-mode      chromatography. Patent family.

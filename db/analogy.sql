/*
 Navicat Premium Data Transfer

 Source Server         : mysql8.0
 Source Server Type    : MySQL
 Source Server Version : 80030
 Source Host           : localhost:3307
 Source Schema         : analogy

 Target Server Type    : MySQL
 Target Server Version : 80030
 File Encoding         : 65001

 Date:
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for pre_map
-- ----------------------------
DROP TABLE IF EXISTS `pre_map`;
CREATE TABLE `pre_map`  (
  `id` int NOT NULL,
  `word1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `word2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `word3` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `word4` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `estimate_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `kind` tinyint NULL DEFAULT NULL,
  `bert_cosine_similarity` double NULL DEFAULT NULL,
  `bert_distance_similarity` double NULL DEFAULT NULL,
  `word2vec_cosine_similarity` double NULL DEFAULT NULL,
  `word2vec_distance_similarity` double NULL DEFAULT NULL,
  `bert_cosine_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `bert_distance_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `word2vec_cosine_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `word2vec_distance_word` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of pre_map
-- ----------------------------
INSERT INTO `pre_map` VALUES (1, '北京', '中国', '曼谷', '泰国', '泰国', '国家-首都', 0, 0.8667556, 9.6264105, 0.7318796684692519, 3.038503421518609, '泰国', '泰国', '泰国', '泰国');
INSERT INTO `pre_map` VALUES (2, '罗马', '意大利', '东京', '日本', '日本', '国家-首都', 0, 0.8491384, 11.095156, 0.7214056509175119, 3.02085092477089, '日本', '日本', '日本', '日本');
INSERT INTO `pre_map` VALUES (3, '英国', '伦敦', '法国', '巴黎', '巴黎', '国家-首都', 0, 0.9567998, 5.2207093, 0.8802890794001533, 1.762684998949272, '巴黎', '巴黎', '巴黎', '巴黎');
INSERT INTO `pre_map` VALUES (4, '贝多芬', '音乐家', '康德', '哲学家', '哲学家', '人名-职业', 0, 0.85390705, 10.514256, 0.626130565932562, 3.37681950355879, '哲学家', '哲学家', '哲学家', '哲学家');
INSERT INTO `pre_map` VALUES (5, '马克思', '哲学家', '但丁', '诗人', '诗人', '人名-职业', 0, 0.8460422, 10.819058, 0.47863641010439006, 4.303598232011161, '诗人', '诗人', '诗人', '诗人');
INSERT INTO `pre_map` VALUES (6, '毕加索', '画家', '莫扎特', '作曲家', '作曲家', '人名-职业', 0, 0.85372597, 9.83501, 0.6965193718796566, 3.360160650896866, '作曲家', '作曲家', '作曲家', '作曲家');
INSERT INTO `pre_map` VALUES (7, '鲸鱼', '海洋', '蜘蛛', '网/蛛网/生物育养箱', '网/蛛网/生物育养箱', '动物-栖息地', 0, 0.88572115, 8.864333, 0.5049951044896612, 3.9695218481769885, '蛛网', '蛛网', '蛛网', '蛛网');
INSERT INTO `pre_map` VALUES (8, '猴子', '森林', '鸭子', '池塘/巢', '池塘/巢', '动物-栖息地', 0, 0.8921937, 8.669954, 0.5539176278400412, 3.6782825348996426, '池塘', '池塘', '池塘', '池塘');
INSERT INTO `pre_map` VALUES (9, '蜜蜂', '蜂巢', '兔子', '洞/兔子窝/笼子', '洞/兔子窝/笼子', '动物-栖息地', 0, 0.88755506, 9.409831, 0.6294022490391702, 3.1357641112694083, '兔子窝', '笼子', '兔子窝', '笼子');
INSERT INTO `pre_map` VALUES (10, '黑板', '绿色', '血液', '红色/暗红色', '红色/暗红色', '事物-颜色', 0, 0.7700866, 14.163704, 0.6087800141369949, 4.851634695182145, '红色', '红色', '暗红色', '暗红色');
INSERT INTO `pre_map` VALUES (11, '奶油', '白色', '西红柿', '红色', '红色', '事物-颜色', 0, 0.8767828, 10.702032, 0.644549668591702, 3.7381764820580936, '红色', '红色', '红色', '红色');
INSERT INTO `pre_map` VALUES (12, '卷心菜', '绿色', '煤炭', '黑色', '黑色', '事物-颜色', 0, 0.7384619, 14.105011, 0.48968126851775484, 5.048099915449613, '黑色', '黑色', '黑色', '黑色');
INSERT INTO `pre_map` VALUES (13, '老鼠', '啮齿类动物', '老虎', '猫科动物/猫/野兽/动物/有机体/食肉动物/脊索动物/真骨动物/哺乳动物', '猫科动物/猫/野兽/动物/有机体/食肉动物/脊索动物/真骨动物/哺乳动物', '同义词-动物', 0, 0.92861235, 7.845524, 0.7898264767557106, 2.739099935840027, '哺乳动物', '哺乳动物', '猫科动物', '猫科动物');
INSERT INTO `pre_map` VALUES (14, '山羊', '哺乳动物', '松鼠', '啮齿类动物/脊椎动物/生物/野兽/动物/脊索动物/真骨动物/哺乳动物', '啮齿类动物/脊椎动物/生物/野兽/动物/脊索动物/真骨动物/哺乳动物', '同义词-动物', 0, 0.9346984, 7.2642646, 0.8607873600958955, 2.5915324378553484, '哺乳动物', '哺乳动物', '哺乳动物', '哺乳动物');
INSERT INTO `pre_map` VALUES (15, '猫头鹰', '猛禽', '狼', '犬/脊椎动物/生物/野兽/犬科动物/动物/食肉动物/脊索动物/哺乳动物', '犬/脊椎动物/生物/野兽/犬科动物/动物/食肉动物/脊索动物/哺乳动物', '同义词-动物', 0, 0.8845052, 8.589744, 0.6513278576622457, 3.514041318112763, '犬', '犬', '野兽', '野兽');
INSERT INTO `pre_map` VALUES (16, '海洋', '水', '镜子', '玻璃/青铜', '玻璃/青铜', '同义词-物质', 0, 0.7312117, 13.690446, 0.5385973871267, 4.208004853561931, '玻璃', '玻璃', '玻璃', '玻璃');
INSERT INTO `pre_map` VALUES (17, '衣服', '布料', '草坪', '草/青草', '草/青草', '同义词-物质', 0, 0.8031692, 12.126915, 0.5619426261509054, 3.810915205711322, '青草', '青草', '青草', '青草');
INSERT INTO `pre_map` VALUES (18, '台桌', '木材', '酸奶', '牛奶', '牛奶', '同义词-物质', 0, 0.82819617, 11.044733, 0.6669494245766201, 4.83754320849638, '牛奶', '牛奶', '牛奶', '牛奶');
INSERT INTO `pre_map` VALUES (19, '星系', '宇宙', '倾听者', '观众', '观众', '同义词-成员', 0, 0.7831694, 13.635785, 0.2442611800983687, 5.255525208002328, '观众', '观众', '观众', '观众');
INSERT INTO `pre_map` VALUES (20, '个人', '社会', '音乐家', '乐队/管弦乐队', '乐队/管弦乐队', '同义词-成员', 0, 0.7961283, 13.99084, 0.49261058463175794, 4.716937682058649, '管弦乐队', '管弦乐队', '管弦乐队', '管弦乐队');
INSERT INTO `pre_map` VALUES (21, '学生', '班级', '市', '省/国家', '省/国家', '同义词-成员', 0, 0.81549174, 10.217701, 0.5989843648112699, 3.658766573690581, '省', '省', '省', '省');
INSERT INTO `pre_map` VALUES (22, '害怕', '恐慌', '生气', '暴躁/异常愤怒/愤慨/愤怒/恼火', '暴躁/异常愤怒/愤慨/愤怒/恼火', '同义词-强度', 0, 0.8667688, 9.398719, 0.7061403807126364, 2.692806317836666, '愤怒', '愤怒', '愤怒', '愤怒');
INSERT INTO `pre_map` VALUES (23, '请求', '哀求', '呼叫', '尖叫/嚎叫', '尖叫/嚎叫', '同义词-强度', 0, 0.886863, 9.490386, 0.7159305726634844, 3.576459427202954, '嚎叫', '嚎叫', '尖叫', '尖叫');
INSERT INTO `pre_map` VALUES (24, '晚餐', '盛宴', '小憩', '睡觉/睡眠/沉睡', '睡觉/睡眠/沉睡', '同义词-强度', 0, 0.80429476, 12.750602, 0.3791563846780337, 4.934251709809914, '沉睡', '沉睡', '沉睡', '沉睡');
INSERT INTO `pre_map` VALUES (25, '清楚的', '模糊的', '近的', '遥远的/偏远的/远方的/远的', '遥远的/偏远的/远方的/远的', '反义词-可分级 ', 0, 0.8630208, 10.205377, 0.601936983584408, 3.588740347608792, '远的', '远的', '远', '远');
INSERT INTO `pre_map` VALUES (26, '有趣的', '乏味的', '干燥的', '潮湿的/泥泞的/湿漉漉的/湿的/闷热的', '潮湿的/泥泞的/湿漉漉的/湿的/闷热的', '反义词-可分级 ', 0, 0.88703376, 10.54716, 0.6727305609170795, 3.837253928127468, '潮湿的', '潮湿的', '潮湿', '潮湿');
INSERT INTO `pre_map` VALUES (27, '紧的', '宽松的/松弛的/宽大的/松懈的', '温暖的', '凉爽的/寒冷的/严寒的', '凉爽的/寒冷的/严寒的', '反义词-可分级 ', 0, 0.7705531, 17.81419, 0.2709360440950835, 4.306102238886843, '凉爽的', '凉爽的', '凉爽', '寒冷');
INSERT INTO `pre_map` VALUES (28, '南方', '北方', '潜水', '浮现', '浮现', '反义词-二分类', 0, 0.82186055, 11.572794, 0.18970757867469623, 4.660488367533978, '浮现', '浮现', '浮现', '浮现');
INSERT INTO `pre_map` VALUES (29, '落下', '上升', '出口', '入口/入口通道', '入口/入口通道', '反义词-二分类', 0, 0.7191812, 14.709616, 0.3660516811948295, 5.065117373969726, '入口', '入口', '入口', '入口');
INSERT INTO `pre_map` VALUES (30, '动态的', '静止的', '忘记', '记住/记起/回忆/回想', '记住/记起/回忆/回想', '反义词-二分类', 0, 0.83725035, 11.248916, 0.5078014737741339, 4.664112986754988, '记起', '记起', '记起', '记起');
INSERT INTO `pre_map` VALUES (31, '管理员', '权力', '停战协议', '和平', '和平', '属性$对象状态（名词：名词）', 0, 0.71565133, 15.474987, 0.4660529714546504, 5.678437084439649, '和平', '和平', '和平', '和平');
INSERT INTO `pre_map` VALUES (32, '孩子', '青春', '富翁', '财富', '财富', '属性$对象状态（名词：名词）', 0, 0.81090236, 11.620981, 0.4131082933496451, 4.9069334524056325, '财富', '财富', '财富', '财富');
INSERT INTO `pre_map` VALUES (33, '冠军', '胜利', '社群', '居民', '居民', '属性$对象状态（名词：名词）', 0, 0.7465521, 13.584417, 0.26176098649615315, 4.9366609150454535, '居民', '居民', '居民', '居民');
INSERT INTO `pre_map` VALUES (34, '画家', '绘画', '厨师', '烹饪/煮', '烹饪/煮', '属性$对象：典型动作（名词：动词）', 0, 0.91761893, 7.7022486, 0.7488951361037239, 2.904996866835979, '烹饪', '烹饪', '烹饪', '烹饪');
INSERT INTO `pre_map` VALUES (35, '医生', '治疗', '炸药', '爆炸', '爆炸', '属性$对象：典型动作（名词：动词）', 0, 0.83001405, 11.252294, 0.5687080224669141, 3.9542561341143165, '爆炸', '爆炸', '爆炸', '爆炸');
INSERT INTO `pre_map` VALUES (36, '裁缝', '缝制', '铁铲', '挖/挖掘/挖土', '挖/挖掘/挖土', '属性$对象：典型动作（名词：动词）', 0, 0.8373611, 11.010563, 0.44691451801823845, 4.6679792110243605, '挖土', '挖土', '挖土', '挖土');
INSERT INTO `pre_map` VALUES (37, '洗涤', '清洁', '修剪', '缩短/变短', '缩短/变短', '原因-目的$动作：目标', 0, 0.7925541, 12.247693, 0.2521639028498816, 5.849255443296464, '缩短', '缩短', '变短', '变短');
INSERT INTO `pre_map` VALUES (38, '睡觉', '休息', '慢跑', '锻炼', '锻炼', '原因-目的$动作：目标', 0, 0.8289348, 11.608354, 0.6156944380573288, 4.042680063746756, '锻炼', '锻炼', '锻炼', '锻炼');
INSERT INTO `pre_map` VALUES (39, '打广告', '推广', '呼吸', '生存/活命', '生存/活命', '原因-目的$动作：目标', 0, 0.7736287, 12.660448, 0.33926871627941124, 4.774293270173495, '生存', '生存', '生存', '生存');
INSERT INTO `pre_map` VALUES (40, '洗澡', '清洁', '锻炼', '健康', '健康', '原因-目的$原因：影响', 0, 0.8144337, 11.17504, 0.3789926572099359, 4.58862310304341, '健康', '健康', '健康', '健康');
INSERT INTO `pre_map` VALUES (41, '病菌', '疾病', '问题', '回答/答案/答复', '回答/答案/答复', '原因-目的$原因：影响', 0, 0.8126538, 11.806099, 0.47486006422915145, 4.395003408592601, '回答', '回答', '回答', '回答');
INSERT INTO `pre_map` VALUES (42, '播种', '发芽', '大喊', '生气/愤怒', '生气/愤怒', '原因-目的$原因：影响', 0, 0.82013446, 12.350514, 0.45291179134134985, 4.390236995859954, '生气', '生气', '生气', '生气');
INSERT INTO `pre_map` VALUES (43, '知识', '愚昧', '上锁', '盗窃/偷盗/偷窃/偷', '盗窃/偷盗/偷窃/偷', '原因-目的$预防', 0, 0.7829608, 13.644874, 0.4210206354925243, 4.98119007830969, '偷窃', '偷窃', '偷窃', '偷窃');
INSERT INTO `pre_map` VALUES (44, '金钱', '贫穷', '睡觉', '疲劳/疲倦/劳累', '疲劳/疲倦/劳累', '原因-目的$预防', 0, 0.7912911, 12.742954, 0.44314298146327435, 4.696306105823344, '疲倦', '疲倦', '劳累', '劳累');
INSERT INTO `pre_map` VALUES (45, '疫苗', '病毒', '食物', '饥饿', '饥饿', '原因-目的$预防', 0, 0.7209441, 14.434302, 0.36873860000354974, 5.071549491395853, '饥饿', '饥饿', '饥饿', '饥饿');
INSERT INTO `pre_map` VALUES (46, '苹果', '树', '葡萄', '藤蔓', '藤蔓', '空间-时间$附属物', 0, 0.79202735, 12.780905, 0.5450625755684038, 3.9335464553932082, '藤蔓', '藤蔓', '藤蔓', '藤蔓');
INSERT INTO `pre_map` VALUES (47, '项链', '脖子', '袜子', '脚', '脚', '空间-时间$附属物', 0, 0.7339293, 15.342513, 0.6544374137521801, 3.8106563625217333, '脚', '脚', '脚', '脚');
INSERT INTO `pre_map` VALUES (48, '水龙头', '管道', '轮胎', '汽车/小轿车/车', '汽车/小轿车/车', '空间-时间$附属物', 0, 0.7608633, 13.208809, 0.4583643592611139, 4.771230814793893, '汽车', '汽车', '汽车', '汽车');
INSERT INTO `pre_map` VALUES (49, '公共汽车', '旅客', '动物园', '动物', '动物', '空间-时间$属性：位置', 0, 0.7634496, 13.508249, 0.44995677451066457, 4.429155875849536, '动物', '动物', '动物', '动物');
INSERT INTO `pre_map` VALUES (50, '柜子', '衣服', '花园', '花朵', '花朵', '空间-时间$属性：位置', 0, 0.8402145, 10.779416, 0.33900941888021907, 4.613838886664183, '花朵', '花朵', '花朵', '花朵');
INSERT INTO `pre_map` VALUES (51, '空间', '行星', '面包店', '蛋糕', '蛋糕', '空间-时间$属性：位置', 0, 0.73204917, 14.777792, 0.5091134615703645, 4.8762182747314595, '蛋糕', '蛋糕', '蛋糕', '蛋糕');
INSERT INTO `pre_map` VALUES (52, '酒吧', '喝酒', '卧室', '睡觉', '睡觉', '空间-时间$位置：行为', 0, 0.8207941, 10.722656, 0.6276678828812433, 3.6149329593821937, '睡觉', '睡觉', '睡觉', '睡觉');
INSERT INTO `pre_map` VALUES (53, '法院', '判决', '厨房', '烹饪/烹调/煮饭', '烹饪/烹调/煮饭', '空间-时间$位置：行为', 0, 0.8220551, 10.526419, 0.5141825556322612, 3.959682120674881, '烹调', '烹调', '煮饭', '煮饭');
INSERT INTO `pre_map` VALUES (54, '办公室', '工作', '体育场', '运动', '运动', '空间-时间$位置：行为', 0, 0.81237143, 11.645361, 0.44842123313899007, 4.205763303530598, '运动', '运动', '运动', '运动');
INSERT INTO `pre_map` VALUES (55, '词语', '句子', '丝线', '衬衫/毛衣/衣服', '衬衫/毛衣/衣服', '空间-时间$序列', 0, 0.8239819, 11.988959, 0.37937357859901677, 4.676317099419989, '衬衫', '衬衫', '毛衣', '衣服');
INSERT INTO `pre_map` VALUES (56, '吞食', '消化', '开始', '结束', '结束', '空间-时间$序列', 0, 0.7661537, 12.888629, 0.4889338983267885, 4.273765891802652, '结束', '结束', '结束', '结束');
INSERT INTO `pre_map` VALUES (57, '吸入', '气味', '预映', '电影', '电影', '空间-时间$序列', 0, 0.7554008, 13.165713, 0.3423721112059485, 5.702490879266135, '电影', '电影', '电影', '电影');
INSERT INTO `pre_map` VALUES (58, '婚礼', '婚姻', '春天', '兴旺/繁盛/景气/美好', '兴旺/繁盛/景气/美好', '空间-时间$时间行为', 0, 0.81162316, 11.414839, 0.37854364207464336, 4.917337763361848, '美好', '美好', '美好', '美好');
INSERT INTO `pre_map` VALUES (59, '假期', '旅行', '成年', '责任/义务', '责任/义务', '空间-时间$时间行为', 0, 0.7042522, 15.014927, 0.24727627163672192, 5.175641046256057, '义务', '义务', '责任', '责任');
INSERT INTO `pre_map` VALUES (60, '冬天', '寒冷', '战争', '破环/毁灭/摧毁', '破环/毁灭/摧毁', '空间-时间$时间行为', 0, 0.8166182, 11.21101, 0.6054675192402347, 3.955858002163597, '毁灭', '毁灭', '毁灭', '毁灭');
INSERT INTO `pre_map` VALUES (61, '明显的', '明显地', '自由的', '自由地', '自由地', '语法-形容词-副词', 1, 0.95657486, 5.757037, 0.686090503215252, 3.673491550487017, '自由地', '自由地', '自由地', '自由地');
INSERT INTO `pre_map` VALUES (62, '冷静的', '冷静地', '完整的', '完整地', '完整地', '语法-形容词-副词', 1, 0.9632746, 5.2827883, 0.4553193421954388, 3.66448741909536, '完整地', '完整地', '完整地', '完整地');
INSERT INTO `pre_map` VALUES (63, '有效的', '有效地', '幸运的', '幸运地', '幸运地', '语法-形容词-副词', 1, 0.9387575, 6.7809534, 0.779551661090506, 2.1871563968136223, '幸运地', '幸运地', '幸运地', '幸运地');
INSERT INTO `pre_map` VALUES (64, '可接受的', '不可接受的', '意识到的', '意识不到的', '意识不到的', '语法-形容词-反义词', 1, 0.9436834, 7.5788302, 0.5710251440091645, 4.030934733811707, '意识不到的', '意识不到的', '意识不到', '意识不到');
INSERT INTO `pre_map` VALUES (65, '清楚的', '不清楚的', '舒服的', '不舒服的', '不舒服的', '语法-形容词-反义词', 1, 0.915182, 8.390933, 0.7866206603191532, 2.3166482212587334, '不舒服的', '不舒服的', '不舒服', '不舒服');
INSERT INTO `pre_map` VALUES (66, '令人信服的', '难以信服的', '一致的', '不一致的', '不一致的', '语法-形容词-反义词', 1, 0.91945195, 8.327036, 0.685063496539586, 3.628476543202513, '不一致的', '不一致的', '不一致', '不一致');
INSERT INTO `pre_map` VALUES (67, '坏的', '更坏的', '大的', '更大的', '更大的', '语法-形容词-比较级', 1, 0.9167029, 7.926954, 0.659759116715328, 3.37471067802526, '更大的', '更大的', '更大', '更大');
INSERT INTO `pre_map` VALUES (68, '深的', '更深的', '快的', '更快的', '更快的', '语法-形容词-比较级', 1, 0.94904286, 6.2093644, 0.7734433090660587, 2.5445961961718657, '更快的', '更快的', '更快', '更快');
INSERT INTO `pre_map` VALUES (69, '明亮的', '更明亮的', '便宜的', '更便宜的', '更便宜的', '语法-形容词-比较级', 1, 0.97309864, 4.8342404, 0.7823709164648631, 2.8496872526004515, '更便宜的', '更便宜的', '更便宜', '更便宜');
INSERT INTO `pre_map` VALUES (70, '寒冷的', '最冷的', '黑暗的', '最黑暗的/最黑的', '最黑暗的/最黑的', '语法-形容词-最高级', 1, 0.93926704, 7.486294, 0.6765786459998664, 3.3407662219200804, '最黑暗的', '最黑暗的', '最黑暗', '最黑暗');
INSERT INTO `pre_map` VALUES (71, '好的', '最好的', '差的', '最差的', '最差的', '语法-形容词-最高级', 1, 0.9498857, 6.9488974, 0.48786693623969757, 3.455497308421544, '最差的', '最差的', '最差', '最差');
INSERT INTO `pre_map` VALUES (72, '长的', '最长的', '慢的', '最慢的', '最慢的', '语法-形容词-最高级', 1, 0.9491179, 6.4301195, 0.7663691178910143, 2.8936608167867153, '最慢的', '最慢的', '最慢', '最慢');

-- ----------------------------
-- Table structure for questionare_data_human
-- ----------------------------
DROP TABLE IF EXISTS `questionare_data_human`;
CREATE TABLE `questionare_data_human`  (
  `id` int NOT NULL,
  `info_id` int NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `question` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `answer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `kind` tinyint NULL DEFAULT NULL,
  `score1` tinyint NULL DEFAULT NULL,
  `score2` tinyint NULL DEFAULT NULL,
  `score3` tinyint NULL DEFAULT NULL,
  `final_score` tinyint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of questionare_data_human
-- ----------------------------

-- ----------------------------
-- Table structure for questionare_data_model
-- ----------------------------
DROP TABLE IF EXISTS `questionare_data_model`;
CREATE TABLE `questionare_data_model`  (
  `id` int NOT NULL,
  `info_id` int NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `question` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `answer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `reason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `kind` tinyint NULL DEFAULT NULL,
  `bert_euc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `bert_cos` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `bert_euc_score` tinyint NULL DEFAULT NULL,
  `bert_cos_score` tinyint NULL DEFAULT NULL,
  `word2vec_euc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `word2vec_cos` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `word2vec_euc_score` tinyint NULL DEFAULT NULL,
  `word2vec_cos_score` tinyint NULL DEFAULT NULL,
  `gpt_euc` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gpt_cos` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gpt_euc_score` tinyint NULL DEFAULT NULL,
  `gpt_cos_score` tinyint NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of questionare_data_model
-- ----------------------------
-- ----------------------------
-- Table structure for questionare_info
-- ----------------------------
DROP TABLE IF EXISTS `questionare_info`;
CREATE TABLE `questionare_info`  (
  `id` int NOT NULL,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `school` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `academy` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `grade` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `class` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `stu_no` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `gender` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `phone` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `spend_time` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of questionare_info
-- ----------------------------

SET FOREIGN_KEY_CHECKS = 1;

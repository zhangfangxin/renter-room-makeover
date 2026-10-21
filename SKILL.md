---
name: renter-room-makeover-optimized
description: 合租房/出租房低成本改造设计 - 优化版，适配主流大模型应用。基于照片解读户型与格局，输出低预算、可逆免破坏、兼顾风水与环境心理学的分区改造方案、采购清单与分期执行计划。优化了提示工程、数据结构化、多平台兼容性和错误处理。
tags: [rental, interior-design, low-budget, fengshui, ai-optimized]
compatible_with: [openai/gpt, anthropic/claude, google/gemini, deepseek]
---

# 合租房改造设计 - 优化版

## 🎯 核心优化点

1. **标准化提示模板** - 适配 GPT、Claude、Gemini 等主流模型
2. **结构化数据输出** - JSON Schema + Markdown 双输出模式
3. **多平台兼容** - 支持 KiroCrew、LangChain、AutoGen 等框架
4. **智能错误处理** - 优雅处理信息缺失和边界情况
5. **性能优化** - 更高效的处理流程和记忆管理

## 📋 工作流程（优化版）

### 阶段 0：智能上下文分析
```yaml
input_analysis:
  has_photos: boolean
  has_budget: boolean  
  has_floor_plan: boolean
  user_expertise_level: [beginner, intermediate, advanced]
  preferred_output_format: [markdown, html, structured_json]
```

### 阶段 1：自适应信息采集
根据输入自动调整采集策略：

**A. 智能拍摄引导**（根据已有信息动态调整）
```prompt
基于以下已有信息：{{existing_info}}
请用户补充以下照片（按优先级排序）：
{{dynamic_photo_list}}
```

**B. 智能问卷生成**（基于缺失的关键信息）
- 预算区间（如未提供）
- 租期剩余时间  
- 可动性限制（能否打孔/粘贴）
- 居住痛点优先级

### 阶段 2：结构化房间档案
采用标准化 JSON Schema：

```json
{
  "room_analysis": {
    "dimensions": {
      "estimated_area_m2": {"value": number, "confidence": number},
      "ceiling_height_m": {"value": number, "confidence": number}
    },
    "orientation": {
      "primary_direction": "north|south|east|west",
      "sunlight_hours": {"morning": number, "afternoon": number}
    },
    "constraints": {
      "budget_cap_yuan": number,
      "damage_level_allowed": "L0|L1|L2|L3",
      "portability_required": boolean
    },
    "furniture": {
      "fixed": [{"name": string, "position": string, "condition": string}],
      "movable": [{"name": string, "dimensions": string, "condition": string}]
    }
  }
}
```

### 阶段 3：多模型兼容的问题诊断
采用模型无关的问题分类：

```yaml
problem_categories:
  - layout: 布局问题（动线、分区、视野）
  - lighting: 照明问题（色温、亮度、层次）
  - storage: 收纳问题（容量、便利性、整洁度）
  - comfort: 舒适度问题（噪音、温度、湿度）
  - aesthetic: 美观问题（色彩、风格、协调性）
  - fengshui: 风水问题（床位、门窗、梁柱）
  
diagnosis_format:
  problem: string
  impact_level: ["critical", "high", "medium", "low"]
  root_cause: string
  solution_constraints: array
  ai_confidence: number
```

### 阶段 4：模块化方案生成
**4.1 布局优化模块**
- SVG/ASCII 平面图生成
- 家具摆放模拟
- 动线优化算法

**4.2 风水优化模块**（理性版）
```python
# 风水规则引擎（可配置）
fengshui_rules = {
  "bed_position": "not_facing_door|back_to_wall|no_beam_above",
  "work_position": "facing_favorable_direction|good_lighting",
  "door_position": "not_blocked|clean_entrance"
}
```

**4.3 预算优化模块**
- 智能物品推荐（基于预算和约束）
- 平替算法（高价→低价替代品）
- 分期购买建议

### 阶段 5：多格式输出
**5.1 Markdown 标准输出**（兼容所有平台）
**5.2 JSON 结构化输出**（供程序化处理）
**5.3 HTML 可视化输出**（交互式方案页面）
**5.4 API 响应格式**（REST/GraphQL 兼容）

### 阶段 6：智能跟进
- 执行进度跟踪
- 二次优化建议
- 退租复原清单生成

## 🛠️ 技术优化特性

### 1. 提示工程优化
```python
# 统一提示模板
prompt_templates = {
  "openai": {
    "system": "你是一个专业的室内设计师，擅长合租房改造...",
    "user": "基于以下房间信息...",
    "response_format": {"type": "json_object"}
  },
  "claude": {
    "system": "<thinking>作为专业室内设计师...</thinking>",
    "user": "Human: 请分析这个房间...",
    "assistant": "Assistant: "
  },
  "gemini": {
    "context": "你是一位经验丰富的...",
    "examples": [{"input": "...", "output": "..."}]
  }
}
```

### 2. 错误处理优化
```python
error_handling = {
  "missing_info": {
    "strategy": "progressive_disclosure",
    "fallback": "generic_advice",
    "confidence_adjustment": True
  },
  "ambiguous_photo": {
    "strategy": "multi_hypothesis",
    "confidence_scoring": True,
    "user_verification": True
  },
  "constraint_conflict": {
    "strategy": "constraint_relaxation",
    "priority_order": ["safety", "budget", "portability", "aesthetics"]
  }
}
```

### 3. 性能优化
- **流式处理**：大照片分批分析
- **缓存机制**：相似房间模式复用
- **并行处理**：多模块同时计算
- **记忆优化**：上下文窗口管理

## 📊 适配主流框架

### LangChain 适配器
```python
from langchain.schema import SystemMessage, HumanMessage
from langchain.chat_models import ChatOpenAI

class RentalRoomMakeoverChain:
    def __init__(self, model="gpt-4"):
        self.llm = ChatOpenAI(model=model)
        self.prompt = self._build_prompt()
        
    def _build_prompt(self):
        return [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=room_info)
        ]
```

### AutoGen 适配器
```python
from autogen import AssistantAgent, UserProxyAgent

rental_designer = AssistantAgent(
    name="rental_designer",
    system_message=RENTAL_DESIGNER_SYSTEM_MESSAGE,
    llm_config={"config_list": config_list}
)
```

### KiroCrew 原生集成
```yaml
# .kiro/crew/skills/renter-room-makeover/config.yaml
integration:
  memory_store: "rental_design_patterns"
  tool_registry: ["photo_analysis", "budget_calculator", "layout_generator"]
  cron_jobs: ["weekly_followup"]
```

## 🧪 测试套件

### 单元测试
```python
def test_photo_analysis():
    """测试照片分析准确性"""
    result = analyze_photos(test_photos)
    assert result["area"]["confidence"] > 0.7
    
def test_budget_optimization():
    """测试预算优化算法"""
    plan = optimize_budget(items, budget_cap=500)
    assert plan["total_cost"] <= 500
```

### 集成测试
- 端到端工作流测试
- 多模型兼容性测试
- 性能基准测试

### 用户测试场景
1. **新手用户**：只有照片，无专业知识
2. **进阶用户**：有明确需求和预算
3. **批量处理**：多房间同时优化

## 📈 性能指标

| 指标 | 目标值 | 当前值 |
|------|--------|--------|
| 照片分析准确率 | >85% | 待测试 |
| 方案生成时间 | <30秒 | 待测试 |
| 用户满意度 | >4.5/5 | 待测试 |
| 跨模型一致性 | >90% | 待测试 |

## 🔄 部署指南

### 快速部署
```bash
# 克隆仓库
git clone https://github.com/your-org/renter-room-makeover-optimized.git

# 安装依赖
pip install -r requirements.txt

# 配置模型API密钥
export OPENAI_API_KEY=your_key
export ANTHROPIC_API_KEY=your_key

# 运行测试
pytest tests/

# 启动服务
python serve.py --port 8080
```

### Docker 部署
```dockerfile
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "serve.py"]
```

## 🤝 贡献指南

1. Fork 仓库
2. 创建功能分支
3. 添加测试用例
4. 提交 Pull Request
5. 通过 CI/CD 检查

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 📞 支持

- 问题报告：GitHub Issues
- 功能请求：GitHub Discussions
- 文档：docs/ 目录
- 示例：examples/ 目录
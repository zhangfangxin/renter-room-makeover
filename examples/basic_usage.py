#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合租房改造设计优化版 - 基本使用示例
演示如何在不同大模型平台上使用本技能
"""

import json
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

def example_openai():
    """OpenAI GPT 使用示例"""
    print("=== OpenAI GPT 示例 ===")
    
    # 模拟房间信息
    room_info = {
        "photos": ["room_photo1.jpg", "room_photo2.jpg"],
        "budget": 500,
        "constraints": {
            "no_drilling": True,
            "portable": True,
            "damage_level_allowed": "L1"
        },
        "room_type": "合租主卧",
        "rental_period": "6个月"
    }
    
    print(f"房间信息: {json.dumps(room_info, indent=2, ensure_ascii=False)}")
    
    # 提示模板（实际使用中会从配置文件加载）
    prompt_template = """你是一个专业的合租房改造设计师。请根据以下房间信息生成改造方案：

房间信息:
{room_info}

约束条件:
1. 预算上限: ¥{budget}
2. 破坏等级: {damage_level}
3. 可带走要求: {portable}
4. 风水调整: 理性讲，用环境心理学解释

请按照以下格式输出:
1. 房间分析
2. 问题诊断
3. 改造方案
4. 采购清单
5. 执行计划"""

    # 实际使用中，这里会调用 OpenAI API
    print("\n提示模板已准备，准备调用模型...")
    
    # 模拟响应
    mock_response = """# 合租主卧改造方案

## 1. 房间分析
- 面积估算: 12㎡ ± 10%
- 朝向: 南向，采光良好
- 现有家具: 床(1.5m)、衣柜、书桌

## 2. 问题诊断
1. **照明单一** - 只有吸顶灯，无层次感
2. **收纳不足** - 物品堆放在地面
3. **个人痕迹缺失** - 缺少个性化装饰

## 3. 改造方案
### A. 灯光改造
- 添加暖光灯带 [L1 ¥35-60 ★可带走]
- 床头阅读灯 [L0 ¥50-80 ★可带走]

### B. 收纳优化
- 床下收纳箱 [L0 ¥40-60 ★可带走]
- 门后挂钩 [L1 ¥15-25 ★可带走]

## 4. 采购清单
| 物品 | 单价 | 数量 | 小计 | 破坏等级 | 可带走 |
|------|------|------|------|----------|--------|
| 暖光灯带 | ¥35-60 | 1 | ¥35-60 | L1 | ★ |
| 床头灯 | ¥50-80 | 1 | ¥50-80 | L0 | ★ |
| 床下箱 | ¥40-60 | 2 | ¥80-120 | L0 | ★ |
| 门后挂钩 | ¥15-25 | 1 | ¥15-25 | L1 | ★ |

**总计: ¥180-285** (在预算 ¥500 内)

## 5. 执行计划
- **Day 1**: 清理、归位、调整床向
- **Week 1**: 安装灯带、挂钩
- **Month 1**: 慢慢添加装饰品"""
    
    print("\n模型响应:")
    print(mock_response)

def example_claude():
    """Anthropic Claude 使用示例"""
    print("\n=== Anthropic Claude 示例 ===")
    
    # Claude 特定的提示格式
    claude_prompt = """Human: 请作为专业室内设计师，帮我分析合租房的改造方案。

房间照片: 已提供
预算: ¥500
约束: 不打孔、物品可带走
租期: 6个月

请输出详细的改造方案，包括房间分析、问题诊断、具体建议和预算分配。

Assistant: """
    
    print("Claude 提示已准备")
    print("提示内容:", claude_prompt[:100] + "...")

def example_gemini():
    """Google Gemini 使用示例"""
    print("\n=== Google Gemini 示例 ===")
    
    # Gemini 对话格式
    gemini_conversation = [
        {
            "role": "user",
            "parts": [{
                "text": """请作为合租房改造专家，基于以下信息提供建议：
1. 照片已上传
2. 预算: ¥500
3. 要求: 不打孔、可带走
4. 租期: 6个月
请输出结构化方案。"""
            }]
        }
    ]
    
    print("Gemini 对话格式已准备")
    print("对话结构:", json.dumps(gemini_conversation, indent=2))

def example_kirocrew():
    """KiroCrew 集成示例"""
    print("\n=== KiroCrew 集成示例 ===")
    
    kirocrew_config = {
        "skill": "renter-room-makeover-optimized",
        "version": "2.0.0",
        "tools": [
            {
                "name": "analyze_photos",
                "description": "分析房间照片，提取格局信息",
                "parameters": {
                    "photos": {"type": "array", "items": {"type": "string"}},
                    "budget": {"type": "number"},
                    "constraints": {"type": "object"}
                }
            },
            {
                "name": "generate_plan",
                "description": "生成改造方案",
                "parameters": {
                    "room_analysis": {"type": "object"},
                    "output_format": {"type": "string", "enum": ["markdown", "json", "html"]}
                }
            }
        ]
    }
    
    print("KiroCrew 工具配置:")
    print(json.dumps(kirocrew_config, indent=2, ensure_ascii=False))

def main():
    """主函数"""
    print("合租房改造设计优化版 - 使用示例")
    print("=" * 50)
    
    example_openai()
    example_claude()
    example_gemini()
    example_kirocrew()
    
    print("\n" + "=" * 50)
    print("示例演示完成！")
    print("\n要实际使用，您需要：")
    print("1. 安装相应的 SDK (openai, anthropic, google-generativeai)")
    print("2. 配置 API 密钥")
    print("3. 导入相应的适配器模块")

if __name__ == "__main__":
    main()
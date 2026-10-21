#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合租房改造设计引擎 - 核心模块
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class DamageLevel(Enum):
    """破坏等级枚举"""
    L0 = "纯摆放"
    L1 = "可逆粘贴"
    L2 = "免打孔支撑"
    L3 = "微损改造"


class BudgetTier(Enum):
    """预算分档枚举"""
    A = "急救包"
    B = "舒适包"
    C = "进阶包"
    D = "大改"


@dataclass
class RoomConstraints:
    """房间改造约束条件"""
    budget_cap: int = 800  # 预算上限
    damage_level_allowed: DamageLevel = DamageLevel.L1  # 允许的破坏等级
    portable_required: bool = True  # 是否需要可带走
    rental_period_months: int = 12  # 租期（月）
    landlord_permission: bool = False  # 是否有房东许可


@dataclass
class RoomAnalysis:
    """房间分析结果"""
    estimated_area_m2: float
    ceiling_height_m: float
    orientation: str  # 朝向
    sunlight_level: str  # 采光等级
    existing_furniture: List[Dict[str, Any]]
    problem_list: List[Dict[str, Any]]
    constraints: RoomConstraints


@dataclass
class RenovationItem:
    """改造项目"""
    name: str
    price_low: float
    price_high: float
    quantity: int = 1
    tier: BudgetTier = BudgetTier.B
    damage_level: DamageLevel = DamageLevel.L0
    portable: bool = True
    purpose: str = ""
    notes: str = ""

    @property
    def total_price_low(self) -> float:
        return self.price_low * self.quantity

    @property
    def total_price_high(self) -> float:
        return self.price_high * self.quantity


@dataclass
class RenovationPlan:
    """改造方案"""
    title: str
    room_analysis: RoomAnalysis
    items: List[RenovationItem]
    layout_description: str
    execution_timeline: Dict[str, List[str]]
    fengshui_adjustments: List[Dict[str, Any]]
    notes: str = ""

    @property
    def total_cost_low(self) -> float:
        return sum(item.total_price_low for item in self.items)

    @property
    def total_cost_high(self) -> float:
        return sum(item.total_price_high for item in self.items)

    @property
    def portable_percentage(self) -> float:
        if not self.items:
            return 0.0
        portable_count = sum(1 for item in self.items if item.portable)
        return portable_count / len(self.items) * 100


class RoomMakeoverEngine:
    """合租房改造设计引擎"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self._cache = {}
        
    def analyze_room(self, photos: List[str], constraints: RoomConstraints) -> RoomAnalysis:
        """
        分析房间照片
        """
        # 这里应该实现照片分析逻辑
        # 目前返回模拟数据
        
        return RoomAnalysis(
            estimated_area_m2=12.5,
            ceiling_height_m=2.8,
            orientation="南向",
            sunlight_level="B",
            existing_furniture=[
                {"name": "床", "size": "1.5m", "fixed": False},
                {"name": "衣柜", "size": "1.8m", "fixed": True},
                {"name": "书桌", "size": "1.2m", "fixed": False},
            ],
            problem_list=[
                {
                    "problem": "照明单一",
                    "impact": "medium",
                    "description": "只有吸顶灯，无层次感"
                },
                {
                    "problem": "收纳不足",
                    "impact": "high",
                    "description": "物品堆放在地面"
                }
            ],
            constraints=constraints
        )
    
    def generate_plan(self, analysis: RoomAnalysis, style: str = "简约") -> RenovationPlan:
        """
        生成改造方案
        """
        # 根据分析和风格生成方案
        items = [
            RenovationItem(
                name="暖光灯带 5m",
                price_low=35,
                price_high=60,
                tier=BudgetTier.A,
                damage_level=DamageLevel.L1,
                portable=True,
                purpose="主氛围光源"
            ),
            RenovationItem(
                name="床头阅读灯",
                price_low=50,
                price_high=80,
                tier=BudgetTier.A,
                damage_level=DamageLevel.L0,
                portable=True,
                purpose="局部照明"
            ),
            RenovationItem(
                name="床下收纳箱",
                price_low=40,
                price_high=60,
                quantity=2,
                tier=BudgetTier.B,
                damage_level=DamageLevel.L0,
                portable=True,
                purpose="隐藏收纳"
            )
        ]
        
        return RenovationPlan(
            title=f"{style}风格合租房改造方案",
            room_analysis=analysis,
            items=items,
            layout_description="床靠南墙，书桌靠窗，休闲角在东北角",
            execution_timeline={
                "Day 1": ["清理杂物", "调整床向", "规划布局"],
                "Week 1": ["安装灯带", "布置收纳", "添加绿植"],
                "Month 1": ["完善装饰", "优化细节", "建立习惯"]
            },
            fengshui_adjustments=[
                {
                    "issue": "床头靠窗",
                    "solution": "加厚床头板 + 遮光帘",
                    "psychology": "减少背后不可见的不安全感",
                    "reversible": True
                }
            ]
        )
    
    def optimize_budget(self, plan: RenovationPlan, target_budget: int) -> RenovationPlan:
        """
        预算优化
        """
        if plan.total_cost_high <= target_budget:
            return plan
        
        # 按优先级排序：先保留 A 档，然后 B 档，最后考虑 C 档
        items_by_tier = {}
        for item in plan.items:
            items_by_tier.setdefault(item.tier, []).append(item)
        
        # 按 tier 优先级保留
        kept_items = []
        current_cost = 0
        
        for tier in [BudgetTier.A, BudgetTier.B, BudgetTier.C, BudgetTier.D]:
            if tier not in items_by_tier:
                continue
                
            for item in items_by_tier[tier]:
                if current_cost + item.total_price_high <= target_budget:
                    kept_items.append(item)
                    current_cost += item.total_price_high
        
        # 创建优化后的方案
        optimized_plan = RenovationPlan(
            title=plan.title + " (预算优化版)",
            room_analysis=plan.room_analysis,
            items=kept_items,
            layout_description=plan.layout_description,
            execution_timeline=plan.execution_timeline,
            fengshui_adjustments=plan.fengshui_adjustments,
            notes=f"预算优化至 ¥{target_budget}，保留了 {len(kept_items)}/{len(plan.items)} 个项目"
        )
        
        return optimized_plan
    
    def to_markdown(self, plan: RenovationPlan) -> str:
        """
        将方案转换为 Markdown 格式
        """
        lines = []
        lines.append(f"# {plan.title}")
        lines.append("")
        
        # 房间分析
        lines.append("## 房间分析")
        lines.append(f"- 面积估算: {plan.room_analysis.estimated_area_m2}㎡")
        lines.append(f"- 层高: {plan.room_analysis.ceiling_height_m}m")
        lines.append(f"- 朝向: {plan.room_analysis.orientation}")
        lines.append(f"- 采光等级: {plan.room_analysis.sunlight_level}")
        lines.append("")
        
        # 问题列表
        lines.append("## 问题诊断")
        for problem in plan.room_analysis.problem_list:
            lines.append(f"- **{problem['problem']}**: {problem['description']} (影响程度: {problem['impact']})")
        lines.append("")
        
        # 采购清单
        lines.append("## 采购清单")
        lines.append("| 物品 | 单价 | 数量 | 小计 | 档位 | 破坏等级 | 可带走 | 作用 |")
        lines.append("|---|---|---|---|---|---|---|---|")
        
        for item in plan.items:
            lines.append(f"| {item.name} | ¥{item.price_low}-{item.price_high} | {item.quantity} | ¥{item.total_price_low}-{item.total_price_high} | {item.tier.value} | {item.damage_level.value} | {'★' if item.portable else '—'} | {item.purpose} |")
        
        lines.append("")
        lines.append(f"**总计: ¥{plan.total_cost_low}-{plan.total_cost_high}**")
        lines.append(f"可带走比例: {plan.portable_percentage:.1f}%")
        lines.append("")
        
        # 执行时间线
        lines.append("## 执行计划")
        for phase, tasks in plan.execution_timeline.items():
            lines.append(f"### {phase}")
            for task in tasks:
                lines.append(f"- {task}")
        
        # 风水调整
        if plan.fengshui_adjustments:
            lines.append("")
            lines.append("## 风水调整")
            for adj in plan.fengshui_adjustments:
                lines.append(f"- **{adj['issue']}**: {adj['solution']}")
                lines.append(f"  - 心理学解释: {adj['psychology']}")
                lines.append(f"  - 可逆性: {'是' if adj['reversible'] else '否'}")
        
        # 预算检查
        if plan.room_analysis.constraints.budget_cap:
            cap = plan.room_analysis.constraints.budget_cap
            if plan.total_cost_high <= cap:
                lines.append("")
                lines.append(f"✅ 方案控制在预算 ¥{cap} 以内")
            else:
                lines.append("")
                lines.append(f"⚠️ 方案上限价 ¥{plan.total_cost_high} 超出预算 ¥{cap}")
        
        return "\n".join(lines)


def main():
    """示例主函数"""
    engine = RoomMakeoverEngine()
    
    # 设置约束
    constraints = RoomConstraints(
        budget_cap=500,
        damage_level_allowed=DamageLevel.L1,
        portable_required=True,
        rental_period_months=6,
        landlord_permission=False
    )
    
    # 分析房间（模拟）
    analysis = engine.analyze_room(["photo1.jpg", "photo2.jpg"], constraints)
    
    # 生成方案
    plan = engine.generate_plan(analysis, style="简约")
    
    # 预算优化
    if plan.total_cost_high > constraints.budget_cap:
        plan = engine.optimize_budget(plan, constraints.budget_cap)
    
    # 输出 Markdown
    markdown = engine.to_markdown(plan)
    print(markdown)


if __name__ == "__main__":
    main()
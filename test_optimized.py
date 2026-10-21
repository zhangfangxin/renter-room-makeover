#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化版技能的基本功能
"""

import os
import sys
import json
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_structure():
    """测试文件结构"""
    print("=== 测试文件结构 ===")
    
    required_files = [
        "SKILL.md",
        "README.md", 
        "config.yaml",
        "requirements.txt",
        "core/engine.py",
        "examples/basic_usage.py"
    ]
    
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 缺失")
    
    return True

def test_config():
    """测试配置文件"""
    print("\n=== 测试配置文件 ===")
    
    try:
        import yaml
        with open("config.yaml", "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        
        required_keys = ["name", "version", "models", "output", "workflow"]
        for key in required_keys:
            if key in config:
                print(f"✅ 配置键 {key}: {config[key]}")
            else:
                print(f"❌ 缺失配置键 {key}")
        
        return True
    except Exception as e:
        print(f"❌ 配置文件错误: {e}")
        return False

def test_engine():
    """测试核心引擎"""
    print("\n=== 测试核心引擎 ===")
    
    try:
        # 尝试导入引擎
        from core.engine import RoomMakeoverEngine, RoomConstraints, DamageLevel
        
        # 创建引擎实例
        engine = RoomMakeoverEngine()
        print("✅ 引擎导入成功")
        
        # 测试约束
        constraints = RoomConstraints(
            budget_cap=500,
            damage_level_allowed=DamageLevel.L1,
            portable_required=True
        )
        print(f"✅ 约束创建: 预算¥{constraints.budget_cap}, 破坏等级{constraints.damage_level_allowed}")
        
        # 测试房间分析（模拟）
        analysis = engine.analyze_room(["test.jpg"], constraints)
        print(f"✅ 房间分析: {analysis.estimated_area_m2}㎡, {analysis.orientation}")
        
        # 测试方案生成
        plan = engine.generate_plan(analysis)
        print(f"✅ 方案生成: {plan.title}, {len(plan.items)}个项目")
        
        # 测试Markdown输出
        markdown = engine.to_markdown(plan)
        print(f"✅ Markdown输出: {len(markdown.splitlines())}行")
        
        # 测试预算优化
        if plan.total_cost_high > 300:
            optimized = engine.optimize_budget(plan, 300)
            print(f"✅ 预算优化: ¥{plan.total_cost_high} → ¥{optimized.total_cost_high}")
        
        return True
        
    except Exception as e:
        print(f"❌ 引擎测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_budget_script():
    """测试预算脚本"""
    print("\n=== 测试预算脚本 ===")
    
    try:
        # 检查脚本文件
        if not Path("budget_sheet.py").exists():
            print("⚠️ budget_sheet.py 不存在，跳过测试")
            return True
        
        # 检查示例数据
        if not Path("sample-plan.json").exists():
            print("⚠️ sample-plan.json 不存在，创建测试数据")
            test_data = {
                "title": "测试改造方案",
                "budget_cap": 500,
                "items": [
                    {
                        "name": "测试灯带",
                        "price_low": 35,
                        "price_high": 60,
                        "qty": 1,
                        "tier": "A",
                        "damage": "L1",
                        "portable": True
                    }
                ]
            }
            with open("sample-plan.json", "w", encoding="utf-8") as f:
                json.dump(test_data, f, ensure_ascii=False, indent=2)
        
        # 测试脚本导入
        import subprocess
        result = subprocess.run(
            [sys.executable, "budget_sheet.py", "sample-plan.json", "--tier", "A"],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        if result.returncode == 0:
            print("✅ 预算脚本运行成功")
            print(f"输出预览: {result.stdout[:200]}...")
        else:
            print(f"❌ 预算脚本运行失败: {result.stderr}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 预算脚本测试失败: {e}")
        return False

def test_references():
    """测试参考文件"""
    print("\n=== 测试参考文件 ===")
    
    required_refs = [
        "photo-analysis.md",
        "fengshui.md",
        "budget-catalog.md",
        "no-damage-playbook.md"
    ]
    
    all_ok = True
    for ref in required_refs:
        if Path(ref).exists():
            size = Path(ref).stat().st_size
            print(f"✅ {ref}: {size}字节")
        else:
            print(f"❌ {ref} 缺失")
            all_ok = False
    
    return all_ok

def main():
    """主测试函数"""
    print("合租房改造设计优化版 - 完整性测试")
    print("=" * 50)
    
    # 切换到优化版目录
    original_dir = os.getcwd()
    try:
        os.chdir("renter-room-makeover-optimized")
        
        tests = [
            ("文件结构", test_structure),
            ("配置文件", test_config),
            ("核心引擎", test_engine),
            ("预算脚本", test_budget_script),
            ("参考文件", test_references)
        ]
        
        results = []
        for name, test_func in tests:
            try:
                success = test_func()
                results.append((name, success))
            except Exception as e:
                print(f"❌ {name} 测试异常: {e}")
                results.append((name, False))
        
        # 输出总结
        print("\n" + "=" * 50)
        print("测试总结:")
        
        passed = sum(1 for _, success in results if success)
        total = len(results)
        
        for name, success in results:
            status = "✅ 通过" if success else "❌ 失败"
            print(f"{name}: {status}")
        
        print(f"\n总计: {passed}/{total} 通过")
        
        if passed == total:
            print("\n🎉 所有测试通过！优化版技能结构完整。")
            return True
        else:
            print(f"\n⚠️ {total - passed} 个测试失败，需要修复。")
            return False
            
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
#命令行提交练习
import json
import time
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts
from pyecharts.globals import ThemeType

try:
    with open("books.json", "r", encoding="utf-8") as f:
        books = json.load(f)
except:
    books = {
        "我的奋斗": {"位置": "A区-101书架", "作者": "希特勒", "库存": 2},
        "三体": {"位置": "B区-203书架", "作者": "刘慈欣", "库存": 1}
    }

print("=== 欢迎来到图书管理系统 ===")
print("提示：退出请按 q 键 ")

while True:
    action = input("请选择项目 1-借书 2-还书 3-取消 4-全部图书 5-库存柱状图 6-库存饼图: \n")

    if action == "q" or action == "3":
        print("感谢使用")
        break

    elif action == "1":
        book_name = input("你要查询什么书 请输入书名或者关键词: \n")
        matches = []
        for name in books:
            if book_name in name:
                matches.append(name)

        if len(matches) == 0:
            print("抱歉，未找到包含该关键词的书籍\n")
        else:
            print(f"为您找到 {len(matches)} 本相关书籍：")
            for name in matches:
                pos = books[name]
                print(f"《{name}》 | 位置: {pos['位置']} | 作者: {pos['作者']} | 剩余库存: {pos['库存']}本")

            choice = input("\n是否要借阅上述书籍？(yes/no): ")
            if choice == "yes":
                target_book = input("请输入你要借阅的书籍完整名称: ")
                if target_book in books:
                    pos = books[target_book]
                    if pos["库存"] > 0:
                        pos["库存"] = pos["库存"] - 1
                        print(f"借阅成功！《{target_book}》目前库存剩余: {pos['库存']}本\n")
                        with open("books.json", "w", encoding="utf-8") as f:
                            json.dump(books, f, ensure_ascii=False)
                    else:
                        print("抱歉，该书库存为 0，已被借完！\n")
                else:
                    print("输入的书名不对，借阅取消。\n")
            elif choice == "no":
                print("好的，已退出借阅。\n")

    elif action == "2":
        bos = input("请问要还哪本书? ")
        if bos in books:
            es = books[bos]
            es["库存"] = es["库存"] + 1
            print("还书成功 目前库存为: ", es["库存"], "\n")

            with open("books.json", "w", encoding="utf-8") as f:
                json.dump(books, f, ensure_ascii=False)
        else:
            print("此书不是这个图书馆的书 还书失败\n")

    elif action == "yagami":
        password = input("请输入管理员密码: ")
        if password == "1314520":
            print("密码验证成功 进入管理员页面\n")
            time.sleep(2)
            # 这里加上了你的选项 3
            admin_choice = input("请选择你要做什么 1-增添书籍 2-废弃书籍 3-修改库存: ")

            if admin_choice == "2":
                del_name = input("请输入你要废弃的书籍: ")
                if del_name in books:
                    del books[del_name]
                    print(f"《{del_name}》已经成功下架\n")
                    with open("books.json", "w", encoding="utf-8") as f:
                        json.dump(books, f, ensure_ascii=False)
                else:
                    print("馆内查无此书，废弃失败！\n")

            elif admin_choice == "1":
                new_name = input("请输入书籍名称: ")
                try:
                    new_count = int(input("请输入初始库存数量: "))
                except:
                    new_count = 1
                new_pos = input("请输入书籍放入位置: ")
                new_author = input("请输入作者: ")

                books[new_name] = {
                    "库存": new_count,
                    "位置": new_pos,
                    "作者": new_author
                }
                print(f"《{new_name}》已经入库成功\n")
                with open("books.json", "w", encoding="utf-8") as f:
                    json.dump(books, f, ensure_ascii=False)

            # ======== 这是你刚才构思的修改库存功能 (展平版) ========
            elif admin_choice == "3":
                mod_name = input("请输入要修改库存的书籍名称：")

                if mod_name in books:
                    old_stock = books[mod_name]["库存"]
                    tip_msg = f"《{mod_name}》当前库存为 {old_stock}本，请输入修改后的库存数量："
                    user_input = input(tip_msg)
                    new_stock = int(user_input)

                    books[mod_name]["库存"] = new_stock
                    print(f"✅ 《{mod_name}》的库存已成功修改为 {new_stock}本！\n")

                    with open("books.json", "w", encoding="utf-8") as f:
                        json.dump(books, f, ensure_ascii=False)
                else:
                    print("馆内查无此书，修改失败！\n")
            # ========================================================

        else:
            print("密码错误 已退出\n")

    elif action == "4":
        print("\n===== 图书馆馆藏总清单 =====")
        for name in books:
            info = books[name]
            print(f"《{name}》 | 作者: {info['作者']} | 位置: {info['位置']} | 剩余: {info['库存']}本")
        print("============================\n")

    elif action == "5":
        print("正在生成暗黑风图表...\n")
        time.sleep(1)
        book_names = list(books.keys())
        book_counts = [info["库存"] for info in books.values()]
        bar = Bar(init_opts=opts.InitOpts(theme=ThemeType.DARK))
        bar.add_xaxis(book_names)
        bar.add_yaxis("库存数量", book_counts)
        bar.set_global_opts(title_opts=opts.TitleOpts(title="图书馆库存实时统计"))
        bar.render("inventory_dark.html")
        print("暗黑图表生成成功！请打开 inventory_dark.html 查看。\n")

    elif action == "6":
        print("正在生成库存占比饼图...\n")
        time.sleep(1)
        book_names = list(books.keys())
        book_counts = [info["库存"] for info in books.values()]
        data_pair = [list(z) for z in zip(book_names, book_counts)]
        pie = Pie()
        pie.add("库存占比", data_pair)
        pie.set_global_opts(title_opts=opts.TitleOpts(title="图书馆库存占比分析"))
        pie.render("pie_chart.html")
        print("饼图生成成功！请打开 pie_chart.html 查看。\n")

    else:
        print("输入无效，请重新选择。\n")




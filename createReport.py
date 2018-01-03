#-*-coding:utf-8-*-
import os
import sys
import subprocess

# 字符串插入
def InsertStr(originalStr, insert, pos):
    return originalStr[:pos] + insert + originalStr[pos:]

# 重新构造报告的格式
def changehtml(htmlFile):
    # 修改html文件
    with open(htmlFile, 'r+') as f:
        t = f.read()
        t = t.replace('<h2>Environment</h2>', '<h2 style="display:none;">Environment</h2>') # 隐藏Environment

        # 设置默认显示结果是隐藏详情
        funcStartPos = t.find('function add_collapse() {', 0)
        print str(funcStartPos)
        funcEndPos = t.find('function init ()', funcStartPos)
        print str(funcEndPos)
        ifPos = t.find("if (elem.innerHTML === 'Passed') {", funcStartPos, funcEndPos)
        print str(ifPos)
        elsePos = t.find("} else {", ifPos, funcEndPos)
        print str(elsePos)
        myPos = t.find('expandcollapse.classList.add("collapser");', elsePos, funcEndPos)
        t = InsertStr(t, 'extras.classList.add("collapsed");\n			', myPos)

        # 结果总数显示和添加表格框
        pos = t.find(
            '<input checked="true" class="filter" data-test-result="passed" disabled="true" hidden="true" '
            'name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>')
        t = InsertStr(t, '\n    <table id="summary-table">\n		<tr>\n			<td>', pos)

        pos = t.find(
            '<input checked="true" class="filter" data-test-result="skipped" disabled="true" hidden="true" '
            'name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>',
            pos
        )
        t = InsertStr(t, '</td>\n			<td>', pos)

        pos = t.find(
            '<input checked="true" class="filter" data-test-result="failed" hidden="true" name="filter_checkbox" '
            'onChange="filter_table(this)" type="checkbox"/>',
            pos
        )
        t = InsertStr(t, '</td>\n			<td>', pos)

        pos = t.find(
            '<input checked="true" class="filter" data-test-result="error" disabled="true" hidden="true" '
            'name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>',
            pos
        )
        t = InsertStr(t, '</td>\n			<td>', pos)

        pos = t.find(
            '<input checked="true" class="filter" data-test-result="xfailed" disabled="true" hidden="true" '
            'name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>',
            pos
        )
        t = InsertStr(t, '</td>\n			<td>', pos)

        pos = t.find(
            '<input checked="true" class="filter" data-test-result="xpassed" disabled="true" hidden="true" '
            'name="filter_checkbox" onChange="filter_table(this)" type="checkbox"/>',
            pos
        )
        t = InsertStr(t, '</td>\n			<td>', pos)

        pos = t.find('<h2>Results</h2>', pos)
        t = InsertStr(t, '</tr>\n	</table>', pos)

        f.seek(0, 0)
        f.write(t)

    htmlPath = os.path.dirname(htmlFile)
    cssDir = os.path.join(htmlPath, 'assets')
    if not os.path.exists(cssDir):
        os.makedirs(cssDir)

    cssFile = os.path.join(htmlPath, 'assets', 'style.css')
    basePath = os.path.dirname(sys.argv[0])
    newCssFile = os.path.join(basePath, 'style.css')
    open(cssFile, 'wb').write(open(newCssFile, 'rb').read())
    print 'Done'


if __name__ == '__main__':
    me = os.path.basename(sys.argv[0])
    desthtml = ''
    new_argv = ['py.test', ]

    # 查询执行参数
    for i in range(len(sys.argv)):
        print sys.argv[i]

        # 组装py.test运行参数
        if i:
            new_argv.append(sys.argv[i])

        # 获取生成的html路径
        if '--html' in sys.argv[i]:
            desthtml = sys.argv[i].split('=')[1]

    # 参数中没有包含html报告地址
    if not desthtml:
        print 'not foud html output path'
        #sys.exit(1)

    # 调用py.test运行测试用例
    s = subprocess.Popen(new_argv, shell=True)
    s.wait()

    # 未生成html格式的报告，直接退出执行
    if not os.path.exists(desthtml):
        print 'create html report failed'
        sys.exit(0)

    # 修改测试报告的样式
    changehtml(desthtml)
    sys.exit(0)

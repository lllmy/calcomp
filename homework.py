# 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )
# 计算一个字符串数据类型的表达式 ： 整数 小数 加减乘除 小括号
# 不准eval
# 将字符串中所有的空格都去掉
# 使用正则表达式 先匹配最内层的小括号
# 使用正则表达式 匹配最内层括号中最先出现的第一个乘法或者除法的（原子）表达式
# 计算这个原子表达式 '2*3' / '4/50'
# 将乘除法的结果填回表达式中
# 再计算下一个出现的乘除法，直到这个小括号中再也没有乘除
# 计算加减法，替换
# 这个小括号中的所有内容都计算成一个结果
# 实现能计算类似
# 1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )
# 等类似公式的计算器程序
import re
def remove_space(formula):
    '''
    对字符串formula进行去除空字符,对一些特殊的运算符，如：--变成+，+-变成-
    :param formula:
    :return: formula
    '''
    formula=formula.replace(' ','')  #去除空字符
    formula = formula.replace('+-','-')#遇到+- 替换成-
    formula = formula.replace('--','+')#遇到--替换成+
    return formula
def bracket_calc(formula):
    '''
    匹配到的内层括号的计算
    :param formula:
    :return: ret
    '''
    formula=re.sub('[()]','',formula)  #去掉括号
    formula=remove_space(formula)  #对formula的格式进行修改
    opt_plus=re.findall('[+-]',formula) #匹配到+-运算符，是一个列表+，-
    opt_div_list = re.split('[+-]', formula) #将加减分割出去，剩下乘除，列表中有*/
    if opt_div_list[0]=='':#opt_div_list列表第一个字符为空的话，表示第一个数字为负号
        opt_div_list[1]='-'+opt_div_list[1]   #拼接在一起
        del opt_plus[0]#把原来的删除了
        del opt_div_list[0]#删除了
    ret=mer(opt_plus,opt_div_list)# 列表 '+' '-' 运算符 进行合并处理
    opt_plus=ret[0]   #重新赋值
    opt_div_list=ret[1]  #重新赋值
    opt_plus_list=calc_div(opt_div_list)#生成只进行加减运算的列表
    ret=calc_plus(opt_plus,opt_plus_list)#这个时候调用加减运算的函数
    return ret#返回值
def mer(opt_plus,opt_div_list):
    '''
    把列表中的形式'2*','-3*',等这样的形式合并在一起
    :param opt_plus:
    :param opt_div_list:
    :return:
    '''
    for k,v in enumerate(opt_div_list):
        if v.endswith('*') or v.endswith('/'):
            opt_div_list[k]=v+opt_plus[k]+opt_div_list[k+1]#合并拼接在一起
            del opt_div_list[k+1]#把原来的数字删除了
            del opt_plus[k]   #把原来的删除了
            return mer(opt_plus,opt_div_list)#传给mer进行在运算
    return opt_plus,opt_div_list#最后把处理后的返回给调用者
def calc_plus(oper,num_list):
    '''
    计算列表中数字的加减
    :param oper: 运算符列表，只有+、-
    :param num_list: 进行数字运算的列表，这里边的数字运算只有数字和加减
    :return: 返回计算结果
    '''
    num=None #初识num
    for i,j in enumerate(num_list): #对数字列表进行操作，索引和数值
        if num:#如果num存在
            if oper[i-1]=='+':#且遇到+符号时
                num+=float(j)  #进行+的操作
            elif oper[i-1]=='-':#遇到-的时候
                num-=float(j) #进行-的操作
        else:
            num=float(j)
    return num
def calc_div(formula_list):
    '''
    计算公式里边乘除
    :param formula_list: 列表
    :return: 返回结果
    '''
    for k,v in enumerate(formula_list):#对带有*/的列表进行操作
        if '*'in v or '/' in v:  #如果*、/在里边，要先进行分割等操作
            opera=re.findall('[*/]',v)  #找到*、/的列表
            c_list=re.split('[*/]',v)  #分割，里边只剩下数字和+-
            num=None
            for o,p in enumerate(c_list):#开始对里边的进行操作
                if num:
                    if opera[o-1]=='*':#*，就要进行以下操作
                        num*=float(p)
                    elif opera[o-1]=='/':#/就要进行以下操作
                        num/=float(p)
                else:
                    num=float(p)
            formula_list[k]=num
    return formula_list  #返回的列表里边是+-和数字
def calc(formula):
    '''
    主程序：先计算括号里边的值，算出后再算乘除，最后算加减
    :param formula:
    :return: ret
    '''
    while True:
        formula_new=re.search('\([^()]+\)',formula)
        #先匹配到最内层括号
        if formula_new:
            formula_new=formula_new.group()
            #找到内层括号的式子
            ret=bracket_calc(formula_new)
            #计算内层括号里边的值
            formula=formula.replace(formula_new,str(ret))
            #将乘除法的结果填回表达式中
            print("\33[32;1m%s\33[0m" % (formula))
        else:
            ret=bracket_calc(formula)#直接计算
            print("\33[33;1m结果:%s\33[0m" % (ret))   #输出最终结果
            exit()  #程序结束
#程序开端
if __name__=='__main__':
    formula='1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )'
    calc(formula)  #调用主函数开始执行程序


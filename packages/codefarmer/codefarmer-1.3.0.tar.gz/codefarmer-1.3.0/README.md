readme.txt


modelmix.py     执行模型平均和模型按比例融合的功能
		里面有3个函数


		modeladd(pro1,pro2,pro3,model1,model2,model3,PRO_PATH,SUB_PATH)
		参数含义：
			pro1,pro2,pro3——三个比例数值，例如0.5
			model1,model2,model3——三个df格式的模型
			PRO_PATH,SUB_PATH——概率文件和结果文件的保存路径


		modelaverage(file_path,str_path,outfile_path)
		参数含义：
			file_path——单文件路径
			str_path——字符串格式路径
			outfile_path——输出结果文件路径


                vote_prob.py   一个函数，执行投票功能
		vote_prob(path1,path2,path3,path4,ave_path1,ave_path2,ave_path3,ave_path4)
		参数含义：
			path1,path2,path3,path4——四个文件路径
			ave_path1,ave_path2,ave_path3,ave_path4——四个概率文件路径
		

stepbystep.py    
		里面一个主函数main_add()
		执行功能：
			搭建整个代码融合框架，其中调用了modeladd、modelaverage、vote_prob等函数


__init__.py 		在导入包的时候执行，内有依赖模块的导入


pip install -i https://pypi.org/project/ codefarmer==1.0.0 即可安装






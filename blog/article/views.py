from django.shortcuts import render, redirect
from .models import ArticlePost
import markdown
from django.http import HttpResponse

from django.http import HttpResponse
from .forms import ArticlePostForm
from django.contrib.auth.models import User

def article_list(request):
   articles = ArticlePost.objects.all()
   context = {'articles': articles}
   return render(request, 'article/list.html', context)

def article_detail(request, id):
   article = ArticlePost.objects.get(id=id)
   article.body = markdown.markdown(article.body,
      extensions=[
         'markdown.extensions.extra',
         'markdown.extensions.codehilite',
      ])
   context = {'article': article}
   return render(request, 'article/detail.html', context)


def article_create(request):
   if request.method == "POST":
      # 将提交的数据赋值到表单示例中
      article_post_form = ArticlePostForm(data=request.POST)
      # 判断提交的数据是否满足模型要求
      if article_post_form.is_valid():
         # 保存数据，暂时不提交到数据库中
         new_article = article_post_form.save(commit=False)
         # 指定数据库中id=1的用户作为作者
         # 如果你进行过删除数据表的操作，可能会找不到id=1的用户
         # 此时请重新创建用户，并传入此用户的ID
         new_article.author = User.objects.get(id=1)
         # 将文章保存到数据库中
         new_article.save()
         # 完成后返回文章列表
         return redirect("article:article_list")
      else:
         return HttpResponse("表单内容有误，请重新填写")
   else:
      # 创建表单类示例
      article_post_form = ArticlePostForm()
      context = {'article_post_form': article_post_form}
      return render(request, 'article/create.html', context)

def article_delete(request,id):
   # 根据id获取需要删除的文章
   article = ArticlePost.objects.get(id=id)
   # 调用delete方法删除文章
   article.delete()
   # 完成删除后返回文章列表
   return redirect("article:article_list")

# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

def article_update(request, id):
   """
   更新文章视图函数
   通过post方式提交表单，更新title，body字段
   GET方法进入初识话表单页面
   id: 文章的Id
   """
   #获取需要修改为的文章对象
   article = ArticlePost.objects.get(id=id)
   # 判断是否使用post方式提交表单
   if request.method == "POST":
      # 将提交的数据赋值到表单示例
      article_post_form = ArticlePostForm(data=request.POST)
      # 判断提交的数据是否满足模型要求
      if article_post_form.is_valid():
         # 保存新写入的title、body 数据并保存
         article.title = request.POST['title']
         article.body = request.POST['body']
         article.save()
         # 完成购返回修改后的文章中，需传入文章ID
         return redirect("article:article_detail", id=id)
      # 如果这个数据不合法，返回错误信息
      else:
         return HttpResponse("表单内容有误，请重新填写。")
   # 如果用户GET请求获取数据
   else:
      # 创建表单类示例
      article_post_form = ArticlePostForm()
      # 赋值上下文，将article文章对象也传递进去，以便的内容
      context = {'article': article, 'article_post_form': article_post_form}
      # 将响应返回到模板中
      return render(request, 'article/update.html', context)
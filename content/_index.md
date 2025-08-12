    # 这个配置将“层叠”应用到所有子文件夹和文章中
    cascade:
      _build:
        # render: a list page for this section.
        # "always" 意味着即使这个文件夹没有 _index.md，也要为它生成一个列表页
        render: always
        # list: this section's content pages in .Site.Pages.
        # "always" 意味着这个区段会出现在 .Site.Sections 列表中，方便我们遍历
        list: always
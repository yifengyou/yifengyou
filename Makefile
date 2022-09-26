
update:
	python3 main.py generate && cp yifengyou.html README.md
	git add . && git commit -am "update README.md"
	git push

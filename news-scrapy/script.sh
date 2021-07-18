#!/bin/bash

export PATH="${PWD%/[^/]*}/env/bin:$PATH"
echo $PATH
scrapy crawl russia24-news

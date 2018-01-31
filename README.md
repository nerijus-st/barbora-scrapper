# Barbora Scrapper
This script is scrapping barbora website and retrieving products based on input parameters. I created this solely out of interest and learning purposes. It's not complete but it works as written below.

### Usage with example
Let's say you want to know which ice-cream contains lowest sugar.
Execute script from CLI. Follow the questions and input desired parameters. There will be three inputs: category, nutrition and ordering.

![image](https://user-images.githubusercontent.com/11758021/35630598-82185368-06aa-11e8-8101-2ff7f57a63af.png)

Chose category number 6 for ice-cream.

![image](https://user-images.githubusercontent.com/11758021/35630645-a005afba-06aa-11e8-8bb6-d88a25e52791.png)

Then chose nutrition number 3 for sugar.

![image](https://user-images.githubusercontent.com/11758021/35630710-c8fa02fe-06aa-11e8-8aba-cfb33ad8d8ac.png)

Lastly, chose 0 for ascending sorting order.

Then script will parse all ice cream pages (including paginated). Parallelism is not implemented in initial version so this might take a while depending on how many products there are.

![image](https://user-images.githubusercontent.com/11758021/35631308-30f82ef2-06ac-11e8-951e-4bbcdda8f8ee.png)

After done parsing script will print sorted products in your chosen order in the terminal and will also show a little graph of top ten products based on your chosen parameters:

![image](https://user-images.githubusercontent.com/11758021/35631015-78a3a5de-06ab-11e8-97d7-bafaf9f05587.png)

import scrapy

class WrittenQuestionsSpider(scrapy.Spider):
    
    name = "written_questions"
    start_urls = ["https://www.chambredesrepresentants.ma/fr/questions-ecrites/"]
    n_page = 1

    def parse(self, response):
        """ Parse the main questions page
        args:
            response: the response object of the main questions page
        returns:
            a generator of the requests to the question pages
        """
        for question_div in response.css("div.q-block3"):
            question_link = question_div.css("a::attr(href)").get()
            yield response.follow(question_link, callback=self.parse_question)
        # get the next page
        next_page = response.css("ul.pagination li.next a::attr(href)").get()
        if next_page is not None and self.n_page < 3:
            self.n_page += 1
            yield response.follow(next_page, callback=self.parse)
            
    def parse_question(self, response):
        """ Parse the question page
        args:
            response: the response object of the question page
        returns:
            a dict containing the question's data (id, author, date, answer_date, ministry, subject, question)
        """
        question_div = response.xpath("//div[contains(@class, 'q-block1')]")
        first_part = question_div.xpath("./div[1]") # for id, subject and date of answer
        second_part = question_div.xpath("./div[2]") # for author
        third_part = question_div.xpath("./div[3]") # for ministry, date and question
        # get id, subject and date of answer
        id = first_part.xpath("./div[1]//text()").get().strip()[13:]
        subject = first_part.xpath("./div[2]//text()").get().strip()[8:]
        answer_date = first_part.xpath("./div[3]//text()")[-1].get()
        # get author
        author = second_part.xpath("./div[2]//a/text()")[-1].get().strip()
        # get question
        ministry = third_part.xpath("./div[1]/text()")[-1].get().strip()
        date = third_part.xpath("./div[2]/text()")[-1].get().strip()
        question = third_part.xpath("./div[3]/p/text()").get().strip()
        # return the data
        return {
            "id": id,
            "author": author,
            "date": date,
            "answer_date": answer_date,
            "ministry": ministry,
            "subject": subject,
            "question": question
        }

import os

from crawling_gocd.calculator import Calculator
from crawling_gocd.crawler import Crawler, CrawlingDataMapper
from crawling_gocd.gocd_domain import Organization
from crawling_gocd.inputs_parser import InputsParser


class Portal:
    def __init__(self):
        self.inputsParser = InputsParser("crawling-gocd.yaml")
        self.calculator = self.assembleCalculator()
        self.output = self.newOutputInstance()
        self.crawler = self.newCrawler()
        self.globalTimeRange = self.getGlobalTimeRange()

    def serve(self):
        input_pipelines = self.inputsParser.parsePipelineConfig()
        pipeline_with_full_data = list(map(lambda pipeline: self.crawlingSinglePipeline(
            pipeline, self.crawler), input_pipelines))

        results = self.calculator.work(pipeline_with_full_data, [])

        for o in self.output:
            o.output(results, self.globalTimeRange)

    def crawlingSinglePipeline(self, pipeline, crawler):
        mapper = CrawlingDataMapper()
        histories = crawler.getPipelineHistories(
            pipeline.name, pipeline.calcConfig.startTime, pipeline.calcConfig.endTime)
        pipeline.histories = mapper.mapPipelineHistory(histories)
        return pipeline

    def newCrawler(self):
        orgnization = Organization(
            os.environ["GOCD_SITE"], os.environ["GOCD_USER"], os.environ["GOCD_PASSWORD"])
        return Crawler(orgnization)

    def assembleCalculator(self):
        inputMetricClasses = self.inputsParser.getMetrics()
        handlers = list(map(lambda clazz: clazz(), inputMetricClasses))
        return Calculator(handlers)

    def newOutputInstance(self):
        input_output_classes = self.inputsParser.outputCustomizeClazz()
        results = []
        for o in input_output_classes:
            results.append(o())
        return results

    def getGlobalTimeRange(self):
        return self.inputsParser.getGlobalTimeRange()

# Make custom API http://drest.readthedocs.org/en/latest/customization.html
import drest
import logging
import ValidicApi

api = ValidicApi.Client("test");
#test = api.simpleGet()
foo = api.api.fitness.get()
api = ValidicApi.Client("test").getApiWithParamsCustom;
bar = api.fitness.some_custom_function()
from django import forms

from catalog.models import Product, Version
from config.settings import UNVALID_WORDS


def string_to_words(my_str: str) -> list:
    """
    Функция преобразует строку в список слов, используется для валидации - поиске запрещенных слов
    В список включаются слова длиннее одной буквы с переводом в нижний регистр, без знаков препинания
    """
    output: list = my_str.split()
    output_list: list = []

    for item in output:
        word: str = ''

        for char in item:
            if char.isalpha():
                word += char
        if len(word) > 1:
            output_list.append(word.lower())
    return output_list


class ProductForm(forms.ModelForm):
    """
    Форма для товара
    """
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        """
        Валидация названия товара
        """
        cleaned_data = self.cleaned_data['name']
        cleaned_data_list = string_to_words(cleaned_data)
        for word in cleaned_data_list:
            if word in UNVALID_WORDS:
                raise forms.ValidationError('Текст содержит недопустимые слова')
        return cleaned_data

    def clean_description(self):
        """
        Валидация описания товара
        """
        cleaned_data = self.cleaned_data['description']
        cleaned_data_list = string_to_words(cleaned_data)
        for word in cleaned_data_list:
            if word in UNVALID_WORDS:
                raise forms.ValidationError('Текст содержит недопустимые слова')
        return cleaned_data


class VersionForm(forms.ModelForm):
    """
    Форма для версии товара
    """
    class Meta:
        model = Version
        fields = '__all__'

(function (global, factory) {
  if (typeof define === "function" && define.amd) {
    define('element/locale/ua', ['module', 'exports'], factory);
  } else if (typeof exports !== "undefined") {
    factory(module, exports);
  } else {
    var mod = {
      exports: {}
    };
    factory(mod, mod.exports);
    global.ELEMENT.lang = global.ELEMENT.lang || {}; 
    global.ELEMENT.lang.ua = mod.exports;
  }
})(this, function (module, exports) {
  'use strict';

  exports.__esModule = true;
  exports.default = {
    el: {
      colorpicker: {
        confirm: 'OK',
        clear: 'Очистити'
      },
      datepicker: {
        now: 'Зараз',
        today: 'Сьогодні',
        cancel: 'Відміна',
        clear: 'Очистити',
        confirm: 'OK',
        selectDate: 'Вибрати дату',
        selectTime: 'Вибрати час',
        startDate: 'Дата початку',
        startTime: 'Час початку',
        endDate: 'Дата завершення',
        endTime: 'Час завершення',
        prevYear: 'Попередній Рік',
        nextYear: 'Наступний Рік',
        prevMonth: 'Попередній Місяць',
        nextMonth: 'Наступний Місяць',
        year: '',
        month1: 'Січень',
        month2: 'Лютий',
        month3: 'Березень',
        month4: 'Квітень',
        month5: 'Травень',
        month6: 'Червень',
        month7: 'Липень',
        month8: 'Серпень',
        month9: 'Вересень',
        month10: 'Жовтень',
        month11: 'Листопад',
        month12: 'Грудень',
        week: 'тиждень',
        weeks: {
          sun: 'Нд',
          mon: 'Пн',
          tue: 'Вт',
          wed: 'Ср',
          thu: 'Чт',
          fri: 'Пт',
          sat: 'Сб'
        },
        months: {
          jan: 'Січ',
          feb: 'Лют',
          mar: 'Бер',
          apr: 'Кві',
          may: 'Тра',
          jun: 'Чер',
          jul: 'Лип',
          aug: 'Сер',
          sep: 'Вер',
          oct: 'Жов',
          nov: 'Лис',
          dec: 'Гру'
        }
      },
      select: {
        loading: 'Завантаження',
        noMatch: 'Співпадінь не знайдено',
        noData: 'Немає даних',
        placeholder: 'Обрати'
      },
      cascader: {
        noMatch: 'Співпадінь не знайдено',
        loading: 'Завантаження',
        placeholder: 'Обрати',
        noData: 'Немає даних'
      },
      pagination: {
        goto: 'Перейти',
        pagesize: 'на сторінці',
        total: 'Всього {total}',
        pageClassifier: ''
      },
      messagebox: {
        title: 'Повідомлення',
        confirm: 'OK',
        cancel: 'Відміна',
        error: 'Неприпустимий ввід даних'
      },
      upload: {
        deleteTip: 'натисніть кнопку щоб видалити',
        delete: 'Видалити',
        preview: 'Перегляд',
        continue: 'Продовжити'
      },
      table: {
        emptyText: 'Немає даних',
        confirmFilter: 'Підтвердити',
        resetFilter: 'Скинути',
        clearFilter: 'Все',
        sumText: 'Сума'
      },
      tree: {
        emptyText: 'Немає даних'
      },
      transfer: {
        noMatch: 'Співпадінь не знайдено',
        noData: 'Обрати',
        titles: ['Список 1', 'Список 2'],
        filterPlaceholder: 'Введіть ключове слово',
        noCheckedFormat: '{total} пунктів',
        hasCheckedFormat: '{checked}/{total} вибрано'
      },
      image: {
        error: 'FAILED' // to be translated
      },
      pageHeader: {
        title: 'Back' // to be translated
      }
    }
  };
  module.exports = exports['default'];
});
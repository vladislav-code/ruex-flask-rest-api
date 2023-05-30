const SERVICES_PRICES = {
  "Orders": [
    {
      "dir": "Оценка и экспертиза",
      "service": "Оценка рыночной стоимости объектов недвижимого имущества",
      "object": "квартира",
      "subject": "для нотариуса",
      "price": 2500,
      "time": "От 1 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "Оценка рыночной стоимости объектов недвижимого имущества",
      "object": "загородный дом",
      "subject": "для органов опеки",
      "price": 2500,
      "time": "От 1 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "До 50 кв.м. Городской район",
      "subject": "Оценка рыночной стоимости недвижимости для страхования",
      "price": 2500,
      "time": "От 2 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "До 50 кв.м. Городской район",
      "subject": "Определение возможных рисков и угроз для объекта недвижимости",
      "price": 2500,
      "time": "От 2 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "50-100 кв.м. Городской район",
      "subject": "Оценка рыночной стоимости недвижимости для принятия управленческих решений",
      "price": 4000,
      "time": "От 2 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "50-100 кв.м. Городской район",
      "subject": "Оценка технического состояния объекта недвижимости",
      "price": 3500,
      "time": "От 2 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "Более 100 кв.м. Городской район",
      "subject": "Оценка рыночной стоимости недвижимости для страхования",
      "price": 6000,
      "time": "От 3 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "Более 100 кв.м. Городской район",
      "subject": "Определение возможных рисков и угроз для объекта недвижимости",
      "price": 7000,
      "time": "От 2 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "Размеры - любые. Загородная местность",
      "subject": "Оценка рыночной стоимости недвижимости для страхования",
      "price": 8000,
      "time": "От 2 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "оценка оборудования (электроэнергетика, нефтегазохимия), машин и механизмов",
      "object": "электроэнергетика",
      "subject": "Предварительный анализ",
      "price": 500,
      "time": "От 1 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "оценка оборудования (электроэнергетика, нефтегазохимия), машин и механизмов",
      "object": "электроэнергетика",
      "subject": "Серийное техническое оборудование",
      "price": 20000,
      "time": "От 5 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "оценка оборудования (электроэнергетика, нефтегазохимия), машин и механизмов",
      "object": "электроэнергетика",
      "subject": "Технологическая линия",
      "price": 40000,
      "time": "От 7 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "предстраховая экспертиза и сюрвей для целей страхования или принятия управленческих решений",
      "object": "Размеры - любые. Загородная местность",
      "subject": "Оценка технического состояния объекта недвижимости",
      "price": 9000,
      "time": "От 2 дней"
    },
  ],
  "Orders2": [
    {
      "dir": "Оценка и экспертиза",
      "service": "оценка ущерба после залива, пожара, иных повреждений (квартиры, дома, ТМЦ, грузы, спецтехника, воздушный и водный транспорт и тд.)",
      "object": "грузовой авто или спецтехника",
      "subject": "",
      "price": 30000,
      "time": "От 3 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "оценка ущерба после залива, пожара, иных повреждений (квартиры, дома, ТМЦ, грузы, спецтехника, воздушный и водный транспорт и тд.)",
      "object": "воздушный или водный транспорт",
      "subject": "",
      "price": 50000,
      "time": "От 3 дней"
    },
    {
      "dir": "Оценка и экспертиза",
      "service": "оценка упущенной выгода и перерывов в производстве",
      "object": "Сельское хозяйство",
      "subject": "",
      "price": 50000,
      "time": "От 2 дней"
    }  
  ]
}

const table = document.getElementById("services-table");

const headerRow = table.insertRow(0);
headerRow.classList.add("table-header");
const headers = ["Направление", "Услуга", "Объект", "Субъект", "Цена", "Срок выполнения"];
for (let i = 0; i < headers.length; i++) {
  const headerCell = headerRow.insertCell(i);
  headerCell.innerHTML = headers[i];
}

for (let i = 0; i < SERVICES_PRICES.Orders.length; i++) {
  const row = table.insertRow(i+1);
  const data = SERVICES_PRICES.Orders[i];
  const cells = [data.dir, data.service, data.object, data.subject, data.price, data.time];

    for (let j = 0; j < cells.length; j++) {
      const cell = row.insertCell(j);
      cell.innerHTML = cells[j];
    }
}

const tableTwo = document.getElementById("services-tabletwo");

const headerRowTwo = tableTwo.insertRow(0);
headerRowTwo.classList.add("table-header");
const headersTwo = ["Направление", "Услуга", "Объект", "Цена", "Срок выполнения"];
for (let i = 0; i < headersTwo.length; i++) {
  const headerCell = headerRowTwo.insertCell(i);
  headerCell.innerHTML = headersTwo[i];
}

for (let i = 0; i < SERVICES_PRICES.Orders2.length; i++) {
  const row = tableTwo.insertRow(i+1);
  const data = SERVICES_PRICES.Orders2[i];
  const cells = [data.dir, data.service, data.object, data.price, data.time];

    for (let j = 0; j < cells.length; j++) {
      const cell = row.insertCell(j);
      cell.innerHTML = cells[j];
    }
}
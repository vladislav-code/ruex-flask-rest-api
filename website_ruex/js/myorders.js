const ORDERS = {
    "Order-1": [
        {
        "dir": "Оценка и экспертиза",
        "service": "Оценка рыночной стоимости объектов недвижимого имущества",
        "object": "загородный дом",
        "subject": "для органов опеки",
        "price": 2500,
        "term": "От 1 дней",
        "status": "оформление",
        "time": "22.05.2023"
        }
    ],
    "Order-2": [
        {
        "dir": "Оценка и экспертиза",
        "service": "оценка ущерба после залива, пожара, иных повреждений (квартиры, дома, ТМЦ, грузы, спецтехника, воздушный и водный транспорт и тд.)",
        "object": "грузовой авто или спецтехника",
        "subject": "",
        "price": 30000,
        "term": "От 2 дней",
        "status": "выполнено",
        "time": "21.05.2023"
        }
    ]
}

//   Создаем заголовок таблицы
const table = document.querySelector(".orders-table");

// Создаем заголовок таблицы
const headerRow = table.insertRow(0);
headerRow.classList.add("table-header");
const headers = ["№", "Направление", "Услуга", "Параметры", "Цена", "Срок", "Статус", "Дата оформления"];
for (let i = 0; i < headers.length; i++) {
  const headerCell = headerRow.insertCell(i);
  headerCell.innerHTML = headers[i];
}

const container = document.querySelector(".myOrders-container");

let index = 1;
for (const orderId in ORDERS) {
  const order = ORDERS[orderId][0];
  const row = table.insertRow();
  row.insertCell(0).innerHTML = index;
  row.insertCell(1).innerHTML = order.dir;
  row.insertCell(2).innerHTML = order.service;
  let objectSubjectValue = order.object;
  if (order.subject !== "") {
    objectSubjectValue += `, ${order.subject}`;
  }
  row.insertCell(3).innerHTML = objectSubjectValue;
  row.insertCell(4).innerHTML = order.price;
  row.insertCell(5).innerHTML = order.term;
  row.insertCell(6).innerHTML = order.status;
  row.insertCell(7).innerHTML = order.time;
  index++;
}

container.appendChild(table);

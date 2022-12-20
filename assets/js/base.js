var date_format = function (value) {
    if (value) {
        return dayjs(value).format('YYYY-MM-DD hh:mm:ss');
    }
    else {
        return value;
    }
 }

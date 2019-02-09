const puppeteer = require('puppeteer');

(async() => {
    let videoUrl = process.argv[process.argv.length - 1];
    if (videoUrl.indexOf('https://avg' + 'le.com/video/') != 0) {
        console.log('Please pass a valid video url');
        process.exit(1);
    }

    const browser = await puppeteer.launch({
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',

            '--enable-logging', '--v=1'
        ]
    });

    const page = await browser.newPage();
    await page.setViewport({
        width: 1920,
        height: 1080,
    });
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36");
    await page.setRequestInterception(true);

    var nextUrl = null;
    page.on('request', interceptedRequest => {
        let url = interceptedRequest._url;
        if (url.indexOf('https://avg' + 'le.com/video-url.php?') > -1) {
            nextUrl = url;
        }
        interceptedRequest.continue();
    });

    await page.goto(videoUrl, {waitUntil: 'networkidle2'});
    const element = await page.$("h1");
    const title = await (await element.getProperty('innerHTML')).jsonValue();

    await page.goto(nextUrl, {waitUntil: 'networkidle2'});
    let urlJson = await page.evaluate(() =>  {
        return JSON.parse(document.querySelector("body").innerText);
    });
    let actualVideoUrl = urlJson['url'];
    console.log(JSON.stringify({
        url: actualVideoUrl,
        title: title,
    }));
    browser.close();
})();

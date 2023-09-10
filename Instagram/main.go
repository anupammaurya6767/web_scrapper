package main

import (
    "log"
    "github.com/sclevine/agouti"
)

type InstagramScraper struct {
    driver *agouti.WebDriver
}

func NewInstagramScraper() *InstagramScraper {
    return &InstagramScraper{}
}

func (s *InstagramScraper) InitializeDriver() error {
    driver := agouti.PhantomJS()
    err := driver.Start()
    if err != nil {
        return err
    }
    s.driver = driver
    return nil
}

func (s *InstagramScraper) ScrapeUserDetails(username string) (map[string]string, error) {
    if s.driver == nil {
        if err := s.InitializeDriver(); err != nil {
            return nil, err
        }
    }

    page, err := s.driver.NewPage()
    if err != nil {
        return nil, err
    }

    err = page.Navigate("https://www.instagram.com/" + username + "/")
    if err != nil {
        return nil, err
    }

    accountDetails, err := page.Find(".-nal3").Elements()
    if err != nil {
        return nil, err
    }

    userDetails := map[string]string{
        "Username":          username,
        "Number of Posts":   accountDetails[0].Text(),
        "Number of Followers": accountDetails[1].Text(),
        "Number of Following": accountDetails[2].Text(),
    }

    return userDetails, nil
}

func (s *InstagramScraper) Close() {
    if s.driver != nil {
        _ = s.driver.Stop()
    }
}

func main() {
    scraper := NewInstagramScraper()
    defer scraper.Close()

    userDetails, err := scraper.ScrapeUserDetails("example_user")
    if err != nil {
        log.Fatal(err)
    }

    log.Println(userDetails)
}

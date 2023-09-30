const axios = require('axios');
const cheerio = require('cheerio');

class Internshala {
    constructor(search_type) {
        this.base_url = 'https://internshala.com/';
        this.search_type = search_type;
    }

    async __scrape_page(url) {
        try {
            const response = await axios.get(url);
            return response.data;
        } catch (error) {
            throw new Error(`An error occurred while fetching the page: ${error.message}`);
        }
    }

    __parse_page(html) {
        try {
            return cheerio.load(html);
        } catch (error) {
            throw new Error(`An error occurred while parsing the page: ${error.message}`);
        }
    }

    async internships() {
        try {
            this.search_type = this.search_type.replace(' ', '%20');
            const url = `${this.base_url}internships/keywords-${this.search_type}`;
            const html = await this.__scrape_page(url);
            const page = this.__parse_page(html);
            const internships = [];

            const internships_container = page('.individual_internship');

            if (!internships_container.length) {
                return { message: 'No internships found' };
            } else {
                internships_container.each((index, element) => {
                    const title = page(element).find('.heading_4_5.profile').text().trim();
                    const company = page(element).find('.heading_6.company_name').text().trim();
                    const location = page(element).find('a.location_link').text().trim();
                    const other_details = page(element).find('.item_body');
                    const duration = other_details.length > 2 ? other_details.eq(1).text().trim() : 'N/A';
                    const stipend_element = page(element).find('.stipend');
                    const stipend = stipend_element.length ? stipend_element.text().trim() : 'N/A';

                    const internship_data = {
                        title,
                        company,
                        location,
                        duration,
                        stipend,
                    };

                    internships.push(internship_data);
                });

                return {
                    data: internships,
                    message: 'Internships are now fetched',
                };
            }
        } catch (error) {
            throw new Error(`An error occurred while scraping internships: ${error.message}`);
        }
    }

    async jobs() {
        try {
            this.search_type = this.search_type.replace(' ', '%20');
            const url = `${this.base_url}jobs/keywords-${this.search_type}`;
            const html = await this.__scrape_page(url);
            const page = this.__parse_page(html);
            const jobs = [];

            const jobs_container = page('#internship_list_container_1');

            if (!jobs_container.text()) {
                return { message: 'No jobs found' };
            } else {
                jobs_container.find('.container-fluid.individual_internship.visibilityTrackerItem').each((index, item) => {
                    const title = page(item).find('.heading_4_5.profile').text().trim();
                    const company = page(item).find('.heading_6.company_name').text().trim();
                    const location = page(item).find('p#location_names').text().trim();
                    const ctc = page(item).find('.item_body.salary').text().trim();
                    const experience = page(item).find('.item_body.desktop-text').text().trim().split(' ')[0];

                    const job_data = {
                        title,
                        company,
                        location,
                        CTC: ctc,
                        'experience(in years)': experience,
                    };

                    jobs.push(job_data);
                });

                return {
                    data: jobs,
                    message: 'Jobs are now fetched',
                };
            }
        } catch (error) {
            throw new Error(`An error occurred while scraping jobs: ${error.message}`);
        }
    }

    async certification_courses() {
        try {
            const url = this.base_url;
            const html = await this.__scrape_page(url);
            const page = this.__parse_page(html);
            const certification_courses = [];

            const certification_section = page('.certification-trainings-section');

            if (certification_section.length) {
                certification_section.find('.card').each((index, card) => {
                    const title_element = page(card).find('h6');
                    const duration_element = page(card).find('span.duration');
                    const rating_element = page(card).find('span.rating');
                    const learners_element = page(card).find('span.learners');
                    const link_element = page(card).find('a');

                    const title = title_element.text().trim() || null;
                    const duration = duration_element.text().trim() || null;
                    const rating = rating_element.text().trim() || null;
                    const learners = learners_element.text().trim() || null;
                    const link = link_element.attr('href') || null;

                    if (title && duration && rating && learners && link) {
                        const certification_data = {
                            title,
                            duration,
                            rating,
                            learners,
                            link,
                        };
                        certification_courses.push(certification_data);
                    }
                });

                return certification_courses;
            } else {
                return null;
            }
        } catch (error) {
            return null;
        }
    }
}

// Example usage:
const search = new Internshala('web development');
search.internships()
    .then(result => console.log(result))
    .catch(error => console.error(error));

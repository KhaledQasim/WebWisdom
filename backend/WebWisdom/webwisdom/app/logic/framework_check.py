
from bs4 import BeautifulSoup
import requests

from selenium import webdriver


from selenium import webdriver
# from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager

    
def WordPress(URL):
    try:
        url = URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        meta_tags = soup.find_all("meta")
        meta_tags_dict = {tag.get('name', tag.get('property', 'No name attribute')): tag.get('content', '') for tag in meta_tags}
        
        if not meta_tags_dict:
            return("No meta tags found that can identify if wordpress is running")
        
        generator = meta_tags_dict.get("generator")
        if generator is not None:
            return meta_tags_dict["generator"]
        else:
            return {"error":"No generator tag found, site might not be using WordPress"}
        
    except Exception as e:
        return {"error":str(e)}


def JavaScriptFrameworkCheck(URL):
  
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()),options=firefox_options)
    driver.get(URL)
    js_code = ""
    js_code = """if(!!window.React || !!document.querySelector('[data-reactroot],[data-reactid]') || Array.from(document.querySelectorAll('*')).some(e => e._reactRootContainer !== undefined || Object.keys(e).some(k => k.startsWith('__reactContainer')))) return 'React.js'; if(!!document.querySelector('script[id=__NEXT_DATA__]')) return 'Next.js'; if(!!document.querySelector('[id=___gatsby]')) return 'Gatsby.js'; if(!!window.angular || !!document.querySelector('.ng-binding,[ng-app],[data-ng-app],[ng-controller],[data-ng-controller],[ng-repeat],[data-ng-repeat]') || !!document.querySelector('script[src*="angular.js"],script[src*="angular.min.js"]')) return 'Angular.js'; if(!!window.getAllAngularRootElements || !!window.ng?.coreTokens?.NgZone) return 'Angular'; if(!!window.Backbone) return 'Backbone.js'; if(!!window.Ember) return 'Ember.js'; if(!!window.Vue) return 'Vue.js'; if(!!window.Meteor) return 'Meteor.js'; if(!!window.Zepto) return 'Zepto.js'; if(!!window.jQuery) return 'jQuery.js';"""
    output = driver.execute_script(js_code)
    print("JavaScript Output:", output)   
    driver.quit()
    return output
    


# javascript code for detecting javascript frameworks

# if(!!window.React ||
#    !!document.querySelector('[data-reactroot], [data-reactid]') ||
#    Array.from(document.querySelectorAll('*')).some(e => e._reactRootContainer !== undefined || Object.keys(e).some(k => k.startsWith('__reactContainer')))
# )
#   console.log('React.js');

# if(!!document.querySelector('script[id=__NEXT_DATA__]'))
#   console.log('Next.js');

# if(!!document.querySelector('[id=___gatsby]'))
#   console.log('Gatsby.js');

# if(!!window.angular ||
#    !!document.querySelector('.ng-binding, [ng-app], [data-ng-app], [ng-controller], [data-ng-controller], [ng-repeat], [data-ng-repeat]') ||
#    !!document.querySelector('script[src*="angular.js"], script[src*="angular.min.js"]')
# )
#   console.log('Angular.js');

# if (!!window.getAllAngularRootElements || !!window.ng?.coreTokens?.NgZone)
#   console.log('Angular');

# if(!!window.Backbone) console.log('Backbone.js');
# if(!!window.Ember) console.log('Ember.js');
# if(!!window.Vue) console.log('Vue.js');
# if(!!window.Meteor) console.log('Meteor.js');
# if(!!window.Zepto) console.log('Zepto.js');
# if(!!window.jQuery) console.log('jQuery.js');


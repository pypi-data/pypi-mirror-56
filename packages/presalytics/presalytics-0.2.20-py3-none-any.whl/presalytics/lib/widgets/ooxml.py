import typing
import time
import urllib.parse
import requests
import presalytics.client.api
import presalytics.story.components
import presalytics.client
import presalytics.lib.exceptions
import presalytics.story.outline


class OoxmlEndpointMap(object):
    BASE_URL = "https://api.presalytics.io/ooxml-automation"

    CHART = "Charts"
    CONNECTION_SHAPE = "ConnectionShapes"
    DOCUMENT = "Documents"
    GROUP = "Groups"
    IMAGE = "Images"
    SHAPE = "Shapes"
    SHAPETREE = "ShapeTrees"
    SLIDE = "Slides"
    TABLE = "Tables"
    THEME = "Themes"

    def __init__(self, endpoint, baseurl: str = None):
        if endpoint not in OoxmlEndpointMap.__dict__.values():
            raise presalytics.lib.exceptions.ValidationError("{0} is not a valid endpoint ID".format(endpoint))
        self.endpoint_id = endpoint
        if not baseurl:
            self.baseurl = OoxmlEndpointMap.BASE_URL
        else:
            self.baseurl = baseurl
        self.root_url = urllib.parse.urljoin(self.baseurl, endpoint)

    def get_id_url(self, id):
        return urllib.parse.urljoin(self.root_url, id)

    def get_svg_url(self, id):
        return urllib.parse.urljoin(self.root_url, "/Svg/" + id)
    
    def get_xml_url(self, id):
        return urllib.parse.urljoin(self.root_url, "/OpenOfficeXml/" + id)


class OoxmlEditorWidget(presalytics.story.components.WidgetBase):
    __component_kind__ = 'ooxml-xml-editor'

    __plugins__ = [
        {
            'name': 'external_scripts',
            'type': 'script',
            'config': {
                'approved_scripts_key': 'ooxml'
            }
        }
    ]

    def __init__(self, name: str, story_id: str, ooxml_id: str, endpoint_map: OoxmlEndpointMap, data: typing.Dict):
        self.story_id = story_id
        self.ooxml_id = ooxml_id
        self.name = name
        self.endpoint_map = endpoint_map
        self.svg_html = self.update(data)
        self.outline_widget = self.serialize()

    def update(self, data: typing.Dict) -> str:
        client = presalytics.client.api.Client()
        auth_header = client.get_auth_header()
        xml_url = self.endpoint_map.get_xml_url(self.ooxml_id)
        xml_response = requests.get(xml_url, headers=auth_header)
        if xml_response.status_code != 200:
            raise presalytics.lib.exceptions.ApiException(default_exception=xml_response.content)
        new_xml = self.update_xml(xml_response.text, data)
        put_data = {
            "id": self.ooxml_id,
            "openOfficeXml": new_xml,
            "type": self.endpoint_map.endpoint_id

        }
        xml_update_response = requests.put(xml_url, put_data, headers=auth_header)
        if xml_response.status_code != 200:
            raise presalytics.lib.exceptions.ApiException(default_exception=xml_update_response.content)
        svg_data = self.get_svg(id)
        return svg_data

    def to_html(self, **kwargs):
        return self.svg_html

    def get_svg(self, id, timeout_iterator=0) -> str:
        svg_url = self.endpoint_map.get_svg_url(id)
        client = presalytics.client.api.Client()
        auth_header = client.get_auth_header()
        response = requests.get(svg_url, headers=auth_header)
        svg_data = response.text
        if response.status_code != 200:
            raise presalytics.lib.exceptions.ApiException(default_exception=response.content)
        if response.text.startswith("Temp data"):
            if timeout_iterator > 5:
                raise presalytics.lib.exceptions.ApiException()
            else:
                time.sleep(2)
                svg_data = self.get_svg(id, timeout_iterator)
        return svg_data
                

    @classmethod
    def deseriailize(cls, component, **kwargs):
        return cls(component.name,
                   component.data["story_id"],
                   component.data["ooxml_id"],
                   component.data["endpoint_id"])

    def serialize(self, **kwargs):
        data = {
            "story_id": self.story_id,
            "ooxml_id": self.ooxml_id,
            "endpoint_id": self.endpoint_map.endpoint_id
        }
        widget = presalytics.story.outline.Widget(
            name=self.name,
            data=data,
            kind=self.__component_kind__
        )
        return widget

    def update_xml(self, old_xml: str, data: typing.Dict):
        raise NotImplementedError


class OoxmlFileWidget(presalytics.story.components.WidgetBase):
    def __init__(self, filename: str, endpoint_id: OoxmlEndpointMap, ):
        self.filename = filename
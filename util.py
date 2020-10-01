from vkwave.bots import BaseEvent
from vkwave.bots.core.dispatching.filters import get_text
from vkwave.bots.core.dispatching.filters.base import FilterResult, BaseFilter
from vkwave.bots.core.dispatching.filters.builtin import AnyText


# A filter that triggers if message starts with specific text
class TextStartsWithFilter(BaseFilter):
    def __init__(self, text: AnyText, ignore_case: bool = True):
        self.text = (text,) if isinstance(text, str) else text
        self.ic = ignore_case

    async def check(self, event: BaseEvent) -> FilterResult:
        text = get_text(event)
        if text is None:
            return FilterResult(False)

        if self.ic:
            text = text.lower()
        return FilterResult(text.startswith(self.text))


# Wrap attachments for vk api. (Could not find functional in VK Wave lib to do this)
# <type><owner_id>_<media_id>
# @ref https://vk.com/dev/messages.send
def wrap_attachments(attachments):
    if not attachments:
        return ""

    return ','.join(
        [item.type + str(item.photo.owner_id) + "_" + str(item.photo.id) for item in attachments if item.photo]
    )

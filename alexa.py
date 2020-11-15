# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.interfaces.audioplayer import (
    PlayDirective, PlayBehavior, AudioItem, Stream)


from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from assistant import SafraAssistant

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response

    assistant = SafraAssistant()
    handler_input.attributes_manager.session_attributes["assistant"] = assistant.serialize()

    speech_text = assistant.start_session()

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("GetBalancesIntent"))
def get_balances_intent_handler(handler_input):
    """Handler for Get Balances Intent."""
    # type: (HandlerInput) -> Response

    assistant = SafraAssistant.deserialize(handler_input.attributes_manager.session_attributes.get("assistant"))
    speech_text = assistant.get_balances()

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("LoginIntent"))
def login_intent_handler(handler_input):
    """Handler for Login Intent."""
    # type: (HandlerInput) -> Response

    assistant = SafraAssistant()
    name = get_slot_value(handler_input=handler_input, slot_name="name")
    speech_text = assistant.login(name)
    handler_input.attributes_manager.session_attributes["assistant"] = assistant.serialize()

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("MakeTransferIntent"))
def make_transfer_intent_handler(handler_input):
    """Handler for Make Transfer Intent."""
    # type: (HandlerInput) -> Response

    name = get_slot_value(handler_input=handler_input, slot_name="name")
    value = float(get_slot_value(handler_input=handler_input, slot_name="value"))
    description = get_slot_value(handler_input=handler_input, slot_name="description")
    assistant = SafraAssistant.deserialize(handler_input.attributes_manager.session_attributes.get("assistant"))
    speech_text = assistant.make_transfer(name, value, description)

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("FindReceivedTransferIntent"))
def find_received_transfer_intent_handler(handler_input):
    """Handler for Find Received Transfer Intent."""
    # type: (HandlerInput) -> Response

    value = float(get_slot_value(handler_input=handler_input, slot_name="value"))
    assistant = SafraAssistant.deserialize(handler_input.attributes_manager.session_attributes.get("assistant"))
    speech_text = assistant.find_received_transfer_by_value(value)

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("FindReceivedTransferFromNameIntent"))
def find_received_transfer_from_name_intent_handler(handler_input):
    """Handler for Find Received Transfer From Name Intent."""
    # type: (HandlerInput) -> Response

    name = get_slot_value(handler_input=handler_input, slot_name="name")
    assistant = SafraAssistant.deserialize(handler_input.attributes_manager.session_attributes.get("assistant"))
    speech_text = assistant.find_received_transfer_from_name(name)

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).set_should_end_session(
        False).response

@sb.request_handler(can_handle_func=is_intent_name("PlayMorningCallIntent"))
def play_morning_call_intent_handler(handler_input):
    """Handler for Play Morning Call Intent."""
    # type: (HandlerInput) -> Response

    assistant = SafraAssistant.deserialize(handler_input.attributes_manager.session_attributes.get("assistant"))
    (speech_text, url) = assistant.play_morning_call()

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).add_directive(
        PlayDirective(
            play_behavior=PlayBehavior.REPLACE_ALL,
            audio_item=AudioItem(
                stream=Stream(
                    token=url,
                    url=url,
                    offset_in_milliseconds=0,
                    expected_previous_token=None)
            )
        )
    ).set_should_end_session(True).response

@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response

    assistant = SafraAssistant.deserialize(handler_input.attributes_manager.session_attributes.get("assistant"))
    speech_text = assistant.get_help()

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Easy Safra", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Easy Safra", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The Hello World skill can't help you with that.  "
        "You can say hello!!")
    reprompt = "You can say hello!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()
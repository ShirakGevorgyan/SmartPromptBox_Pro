from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.states.gpt_states import GPTMemoryStates
from app.llm.assistant import gpt_assistant_conversation
from app.telegram_bot.menu import main_menu, gpt_reply_markup

router = Router()



# ✅ Սկսել GPT զ conversación՝ "⭐️ Talk to me"
@router.message(F.text == "⭐️ Խոսիր ինձ հետ")
async def start_conversation(message: Message, state: FSMContext):
    print("✅ Սկսեց GPT զրույցը")
    await state.set_state(GPTMemoryStates.chatting)
    await state.update_data(chat_history=[], message_ids=[])

    start_msg = await message.answer("🧠 Բարև, գրիր որևէ բան և ես կպատասխանեմ։", reply_markup=gpt_reply_markup)

    # Պահենք այս մեսիջի ID-ն
    await state.update_data(message_ids=[start_msg.message_id])

# ✅ GPT Շարունակություն
@router.message(GPTMemoryStates.chatting)
async def continue_conversation(message: Message, state: FSMContext):
    user_input = message.text
    data = await state.get_data()
    history = data.get("chat_history", [])
    message_ids = data.get("message_ids", [])

    # Վերադառնալ գլխավոր
    if user_input == "🔝 Վերադառնալ գլխավոր մենյու":
        await state.clear()
        await message.answer("🏠 Վերադարձ գլխավոր մենյու։", reply_markup=main_menu)
        return

    # Մաքրել զրույցը
    if user_input == "🧹 Մաքրել զրույցը":
        for mid in message_ids:
            try:
                await message.bot.delete_message(chat_id=message.chat.id, message_id=mid)
            except Exception as e:
                print(f"❌ Failed to delete message {mid}: {e}")
        await state.clear()
        await message.answer("📭 Զրույցը մաքրված է։ Կարող ես սկսել նորից։")
        await state.set_state(GPTMemoryStates.chatting)
        # Պահենք նոր զրույցի ID-ն
        await state.update_data(chat_history=[], message_ids=[])
        start_msg = await message.answer("🧠 Բարև, գրիր որևէ բան և ես կպատասխանեմ։", reply_markup=gpt_reply_markup)
        await state.update_data(message_ids=[start_msg.message_id])
        return

    # ✅ Շարունակել զրույցը
    history.append({"role": "user", "content": user_input})
    wait_msg = await message.answer("🤖 Մտածում եմ...")
    message_ids.append(wait_msg.message_id)

    try:
        reply = await gpt_assistant_conversation(history)
        history.append({"role": "assistant", "content": reply})
        reply_msg = await message.answer(reply)
        message_ids.extend([reply_msg.message_id])

        await state.update_data(chat_history=history, message_ids=message_ids)

    except Exception as e:
        print("GPT Error:", e)
        error_msg = await message.answer("❌ GPT-ից պատասխան ստանալը ձախողվեց։")
        message_ids.append(error_msg.message_id)
        await state.update_data(message_ids=message_ids)


# # ✅ fallback միայն եթե GPT չկասկածի
# @router.message()
# async def fallback_handler(message: Message):
#     await message.answer("🤖 Խնդրում եմ սեղմիր «գպտ» կոճակը՝ սկսելու խելացի զրույց։")

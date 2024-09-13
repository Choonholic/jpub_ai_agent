# 필요 라이브러리 가져오기
import fire

from metagpt.actions import Action, UserRequirement
from metagpt.logs import logger
from metagpt.roles import Role
from metagpt.schema import Message
from metagpt.team import Team

# 주문 처리 작업 정의
class ProcessOrder(Action):
    PROMPT_TEMPLATE: str = """
    Process the following order: {order_details}.
    """
    name: str = "ProcessOrder"

    async def run(self, order_details: str):
        prompt = self.PROMPT_TEMPLATE.format(order_details=order_details)
        rsp = await self._aask(prompt)
        return rsp.strip()

# 주문 처리 역할 정의
class OrderProcessor(Role):
    name: str = "OrderProcessor"
    profile: str = "Process orders"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement])
        self.set_actions([ProcessOrder])

# 재고 관리 작업 정의
class ManageInventory(Action):
    PROMPT_TEMPLATE: str = """
    Update inventory based on the following order: {order_details}.
    """
    name: str = "ManageInventory"

    async def run(self, order_details: str):
        prompt = self.PROMPT_TEMPLATE.format(order_details=order_details)
        rsp = await self._aask(prompt)
        return rsp.strip()

# 재고 관리 역할 정의
class InventoryManager(Role):
    name: str = "InventoryManager"
    profile: str = "Manage inventory"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([ProcessOrder])
        self.set_actions([ManageInventory])

# 고객 서비스 작업 정의
class HandleCustomerService(Action):
    PROMPT_TEMPLATE: str = """
    Handle the following customer service request: {request_details}.
    """
    name: str = "HandleCustomerService"

    async def run(self, request_details: str):
        prompt = self.PROMPT_TEMPLATE.format(request_details=request_details)
        rsp = await self._aask(prompt)
        return rsp.strip()

# 고객 서비스 역할 정의
class CustomerServiceRepresentative(Role):
    name: str = "CustomerServiceRepresentative"
    profile: str = "Handle customer service"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._watch([UserRequirement, ManageInventory])
        self.set_actions([HandleCustomerService])

# main 함수
async def main(
    order_details: str = "A bouquet of red roses",
    investment: float = 3.0,
    n_round: int = 5,
    add_human: bool = False,
):
    logger.info(order_details)

    # 팀 구성 및 역할 추가
    team = Team()
    team.hire(
        [
            OrderProcessor(),
            InventoryManager(),
            CustomerServiceRepresentative(is_human=add_human),
        ]
    )

    # 투자 및 프로젝트 실행
    team.invest(investment=investment)
    team.run_project(order_details)

    # 지정된 라운드 동안 실행
    await team.run(n_round=n_round)

# 프로그램 실행
if __name__ == "__main__":
    fire.Fire(main)

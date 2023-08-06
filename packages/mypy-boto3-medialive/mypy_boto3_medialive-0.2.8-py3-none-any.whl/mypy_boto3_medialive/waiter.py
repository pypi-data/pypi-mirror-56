"Main interface for medialive Waiters"
from __future__ import annotations

from botocore.waiter import Waiter as Boto3Waiter
from mypy_boto3_medialive.type_defs import (
    ChannelCreatedWaitWaiterConfigTypeDef,
    ChannelDeletedWaitWaiterConfigTypeDef,
    ChannelRunningWaitWaiterConfigTypeDef,
    ChannelStoppedWaitWaiterConfigTypeDef,
    MultiplexCreatedWaitWaiterConfigTypeDef,
    MultiplexDeletedWaitWaiterConfigTypeDef,
    MultiplexRunningWaitWaiterConfigTypeDef,
    MultiplexStoppedWaitWaiterConfigTypeDef,
)


__all__ = (
    "ChannelCreatedWaiter",
    "ChannelDeletedWaiter",
    "ChannelRunningWaiter",
    "ChannelStoppedWaiter",
    "MultiplexCreatedWaiter",
    "MultiplexDeletedWaiter",
    "MultiplexRunningWaiter",
    "MultiplexStoppedWaiter",
)


class ChannelCreatedWaiter(Boto3Waiter):
    """
    Waiter for `channel_created` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, ChannelId: str, WaiterConfig: ChannelCreatedWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_channel` every 3 seconds until a successful state
        is reached. An error is returned after 5 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeChannel>`_

        **Request Syntax**
        ::

          waiter.wait(
              ChannelId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type ChannelId: string
        :param ChannelId: **[REQUIRED]** channel ID

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 3

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 5

        :returns: None
        """


class ChannelDeletedWaiter(Boto3Waiter):
    """
    Waiter for `channel_deleted` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, ChannelId: str, WaiterConfig: ChannelDeletedWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_channel` every 5 seconds until a successful state
        is reached. An error is returned after 20 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeChannel>`_

        **Request Syntax**
        ::

          waiter.wait(
              ChannelId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type ChannelId: string
        :param ChannelId: **[REQUIRED]** channel ID

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 20

        :returns: None
        """


class ChannelRunningWaiter(Boto3Waiter):
    """
    Waiter for `channel_running` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, ChannelId: str, WaiterConfig: ChannelRunningWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_channel` every 5 seconds until a successful state
        is reached. An error is returned after 120 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeChannel>`_

        **Request Syntax**
        ::

          waiter.wait(
              ChannelId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type ChannelId: string
        :param ChannelId: **[REQUIRED]** channel ID

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 120

        :returns: None
        """


class ChannelStoppedWaiter(Boto3Waiter):
    """
    Waiter for `channel_stopped` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, ChannelId: str, WaiterConfig: ChannelStoppedWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_channel` every 5 seconds until a successful state
        is reached. An error is returned after 28 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeChannel>`_

        **Request Syntax**
        ::

          waiter.wait(
              ChannelId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type ChannelId: string
        :param ChannelId: **[REQUIRED]** channel ID

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 28

        :returns: None
        """


class MultiplexCreatedWaiter(Boto3Waiter):
    """
    Waiter for `multiplex_created` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, MultiplexId: str, WaiterConfig: MultiplexCreatedWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_multiplex` every 3 seconds until a successful
        state is reached. An error is returned after 5 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeMultiplex>`_

        **Request Syntax**
        ::

          waiter.wait(
              MultiplexId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type MultiplexId: string
        :param MultiplexId: **[REQUIRED]** The ID of the multiplex.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 3

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 5

        :returns: None
        """


class MultiplexDeletedWaiter(Boto3Waiter):
    """
    Waiter for `multiplex_deleted` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, MultiplexId: str, WaiterConfig: MultiplexDeletedWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_multiplex` every 5 seconds until a successful
        state is reached. An error is returned after 20 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeMultiplex>`_

        **Request Syntax**
        ::

          waiter.wait(
              MultiplexId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type MultiplexId: string
        :param MultiplexId: **[REQUIRED]** The ID of the multiplex.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 20

        :returns: None
        """


class MultiplexRunningWaiter(Boto3Waiter):
    """
    Waiter for `multiplex_running` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, MultiplexId: str, WaiterConfig: MultiplexRunningWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_multiplex` every 5 seconds until a successful
        state is reached. An error is returned after 120 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeMultiplex>`_

        **Request Syntax**
        ::

          waiter.wait(
              MultiplexId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type MultiplexId: string
        :param MultiplexId: **[REQUIRED]** The ID of the multiplex.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 120

        :returns: None
        """


class MultiplexStoppedWaiter(Boto3Waiter):
    """
    Waiter for `multiplex_stopped` name.
    """

    # pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
    def wait(
        self, MultiplexId: str, WaiterConfig: MultiplexStoppedWaitWaiterConfigTypeDef = None
    ) -> None:
        """
        Polls :py:meth:`MediaLive.Client.describe_multiplex` every 5 seconds until a successful
        state is reached. An error is returned after 28 failed checks.

        See also: `AWS API Documentation
        <https://docs.aws.amazon.com/goto/WebAPI/medialive-2017-10-14/DescribeMultiplex>`_

        **Request Syntax**
        ::

          waiter.wait(
              MultiplexId='string',
              WaiterConfig={
                  'Delay': 123,
                  'MaxAttempts': 123
              }
          )
        :type MultiplexId: string
        :param MultiplexId: **[REQUIRED]** The ID of the multiplex.

        :type WaiterConfig: dict
        :param WaiterConfig:

          A dictionary that provides parameters to control waiting behavior.

          - **Delay** *(integer) --*

            The amount of time in seconds to wait between attempts. Default: 5

          - **MaxAttempts** *(integer) --*

            The maximum number of attempts to be made. Default: 28

        :returns: None
        """

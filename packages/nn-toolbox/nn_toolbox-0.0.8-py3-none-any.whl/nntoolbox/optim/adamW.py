from torch.optim import Adam
import math
import torch
from typing import Tuple


__all__ = ['AdamW']


class AdamW(Adam):
    """
    Implement decoupled weight decay for Adam. This is no longer maintained, as pytorch already provides its own
    implementation, which is most likely more efficient.

    References:

        https://arxiv.org/abs/1711.05101
    """
    def __init__(
            self, params, lr: float=1e-3, betas: Tuple[float, float]=(0.9, 0.999),
            eps: float=1e-8,weight_decay: float=0.0001, amsgrad: bool=False
    ):
        if not 0.0 < weight_decay:
            raise ValueError("Invalid weight decay: {}".format(weight_decay))
        super(AdamW, self).__init__(params, lr, betas, eps, weight_decay, amsgrad)

    def step(self, closure=None):
        """Performs a single optimization step.

        Arguments:
            closure (callable, optional): A closure that reevaluates the model
                and returns the loss.
        """
        loss = None
        if closure is not None:
            loss = closure()

        for group in self.param_groups:
            for p in group['params']:
                if p.grad is None:
                    continue
                grad = p.grad.data
                if grad.is_sparse:
                    raise RuntimeError('Adam does not support sparse gradients, please consider SparseAdam instead')
                amsgrad = group['amsgrad']

                state = self.state[p]

                # State initialization
                if len(state) == 0:
                    state['step'] = 0
                    # Exponential moving average of gradient values
                    state['exp_avg'] = torch.zeros_like(p.data)
                    # Exponential moving average of squared gradient values
                    state['exp_avg_sq'] = torch.zeros_like(p.data)
                    if amsgrad:
                        # Maintains max of all exp. moving avg. of sq. grad. values
                        state['max_exp_avg_sq'] = torch.zeros_like(p.data)

                exp_avg, exp_avg_sq = state['exp_avg'], state['exp_avg_sq']
                if amsgrad:
                    max_exp_avg_sq = state['max_exp_avg_sq']
                beta1, beta2 = group['betas']

                state['step'] += 1

                # Decay the first and second moment running average coefficient
                exp_avg.mul_(beta1).add_(1 - beta1, grad)
                exp_avg_sq.mul_(beta2).addcmul_(1 - beta2, grad, grad)
                if amsgrad:
                    # Maintains the maximum of all 2nd moment running avg. till now
                    torch.max(max_exp_avg_sq, exp_avg_sq, out=max_exp_avg_sq)
                    # Use the max. for normalizing running avg. of gradient
                    denom = max_exp_avg_sq.sqrt().add_(group['eps'])
                else:
                    denom = exp_avg_sq.sqrt().add_(group['eps'])

                bias_correction1 = 1 - beta1 ** state['step']
                bias_correction2 = 1 - beta2 ** state['step']
                step_size = group['lr'] * math.sqrt(bias_correction2) / bias_correction1

                if group['weight_decay'] != 0: # Decoupled weight decay:
                    p.data.add_(-group['lr'] * group['weight_decay'] * p.data)

                p.data.addcdiv_(-step_size, exp_avg, denom)

        return loss
